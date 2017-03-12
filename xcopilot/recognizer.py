import speech_recognition as sr
import io, os, subprocess, wave, aifc, math, audioop
import collections, threading
import platform, stat
import json, hashlib, hmac, time, base64, random, uuid
import tempfile, shutil

try: # attempt to use the Python 2 modules
    from urllib import urlencode
    from urllib2 import Request, urlopen, URLError, HTTPError
except ImportError: # use the Python 3 modules
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError

class Recognizer(sr.Recognizer):
    def recognize_sphinx2(self, audio_data, language = "xp-XP", keyword_entries = None, show_all = False):
            """
            Performs speech recognition on ``audio_data`` (an ``AudioData`` instance), using CMU Sphinx.

            The recognition language is determined by ``language``, an RFC5646 language tag like ``"en-US"`` or ``"en-GB"``, defaulting to US English. Out of the box, only ``en-US`` is supported. See `Notes on using `PocketSphinx <https://github.com/Uberi/speech_recognition/blob/master/reference/pocketsphinx.rst>`__ for information about installing other languages. This document is also included under ``reference/pocketsphinx.rst``.

            If specified, the keywords to search for are determined by ``keyword_entries``, an iterable of tuples of the form ``(keyword, sensitivity)``, where ``keyword`` is a phrase, and ``sensitivity`` is how sensitive to this phrase the recognizer should be, on a scale of 0 (very insensitive, more false negatives) to 1 (very sensitive, more false positives) inclusive. If not specified or ``None``, no keywords are used and Sphinx will simply transcribe whatever words it recognizes. Specifying ``keyword_entries`` is more accurate than just looking for those same keywords in non-keyword-based transcriptions, because Sphinx knows specifically what sounds to look for.

            Returns the most likely transcription if ``show_all`` is false (the default). Otherwise, returns the Sphinx ``pocketsphinx.pocketsphinx.Decoder`` object resulting from the recognition.

            Raises a ``speech_recognition.UnknownValueError`` exception if the speech is unintelligible. Raises a ``speech_recognition.RequestError`` exception if there are any issues with the Sphinx installation.
            """
            assert isinstance(audio_data, sr.AudioData), "``audio_data`` must be audio data"
            assert isinstance(language, str), "``language`` must be a string"
            assert keyword_entries is None or all(isinstance(keyword, str) and 0 <= sensitivity <= 1 for keyword, sensitivity in keyword_entries), "``keyword_entries`` must be ``None`` or a list of pairs of strings and numbers between 0 and 1"

            # import the PocketSphinx speech recognition module
            try:
                from pocketsphinx import pocketsphinx
                from sphinxbase import sphinxbase
            except ImportError:
                raise sr.RequestError("missing PocketSphinx module: ensure that PocketSphinx is set up correctly.")
            except ValueError:
                raise sr.RequestError("bad PocketSphinx installation detected; make sure you have PocketSphinx version 0.0.9 or better.")

            language_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pocketsphinx-data", language)
            if not os.path.isdir(language_directory):
                raise sr.RequestError("missing PocketSphinx language data directory: \"{0}\"".format(language_directory))
            acoustic_parameters_directory = os.path.join(language_directory, "acoustic-model")
            if not os.path.isdir(acoustic_parameters_directory):
                raise RequestError("missing PocketSphinx language model parameters directory: \"{0}\"".format(acoustic_parameters_directory))
            language_model_file = os.path.join(language_directory, "language-model.lm")
            if not os.path.isfile(language_model_file):
                raise sr.RequestError("missing PocketSphinx language model file: \"{0}\"".format(language_model_file))
            phoneme_dictionary_file = os.path.join(language_directory, "pronounciation-dictionary.dic")
            if not os.path.isfile(phoneme_dictionary_file):
                raise sr.RequestError("missing PocketSphinx phoneme dictionary file: \"{0}\"".format(phoneme_dictionary_file))

            # create decoder object
            config = pocketsphinx.Decoder.default_config()
            config.set_string("-hmm", acoustic_parameters_directory) # set the path of the hidden Markov model (HMM) parameter files
            config.set_string("-lm", language_model_file)
            config.set_string("-dict", phoneme_dictionary_file)
            config.set_string("-logfn", os.devnull) # disable logging (logging causes unwanted output in terminal)
            decoder = pocketsphinx.Decoder(config)

            # obtain audio data
            raw_data = audio_data.get_raw_data(convert_rate = 16000, convert_width = 2) # the included language models require audio to be 16-bit mono 16 kHz in little-endian format

            # obtain recognition results
            if keyword_entries is not None: # explicitly specified set of keywords
                with tempfile_TemporaryDirectory() as temp_directory:
                    # generate a keywords file - Sphinx documentation recommendeds sensitivities between 1e-50 and 1e-5
                    keywords_path = os.path.join(temp_directory, "keyphrases.txt")
                    with open(keywords_path, "w") as f:
                        f.writelines("{} /1e{}/\n".format(keyword, 45 * sensitivity - 50) for keyword, sensitivity in keyword_entries)

                    # perform the speech recognition with the keywords file (this is inside the context manager so the file isn;t deleted until we're done)
                    decoder.set_kws("keywords", keywords_path)
                    decoder.set_search("keywords")
                    decoder.start_utt() # begin utterance processing
                    decoder.process_raw(raw_data, False, True) # process audio data with recognition enabled (no_search = False), as a full utterance (full_utt = True)
                    decoder.end_utt() # stop utterance processing
            else: # no keywords, perform freeform recognition
                decoder.start_utt() # begin utterance processing
                decoder.process_raw(raw_data, False, True) # process audio data with recognition enabled (no_search = False), as a full utterance (full_utt = True)
                decoder.end_utt() # stop utterance processing

            if show_all: return decoder

            # return results
            hypothesis = decoder.hyp()
            if hypothesis is not None: return hypothesis.hypstr
            raise sr.UnknownValueError() # no transcriptions available
