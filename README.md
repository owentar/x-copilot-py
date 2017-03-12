# xcopilot

This is a Python plugin for [X-Plane](http://www.x-plane.com/) to support voice commands in the simulator.

## How does it work?

The process is quite simple:

1. Transcribe voice commands to text using [speech_recognition](https://github.com/Uberi/speech_recognition) project.
2. When the command is in a string format, it's parsed through a regular expression to identify and extract the data from the specified command
3. Once the command is recognized, it's translated to data ref operations (setting / getting one or more data refs in x-plane)

## Pocketsphinx configuration

Currently the language used by sphinx to recognize commands is specified in corpus.txt file.

To create the language model, go to: http://www.speech.cs.cmu.edu/tools/lmtool-new.html, upload the corpus.txt and get the LM and DIC files content and replace the existing ones defined in pockectsphinx-data/xp-XP folder.

## Test

> $ python -m unittest discover
