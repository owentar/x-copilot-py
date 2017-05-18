import threading
import pyaudio
import wave
from array import array
from struct import pack
from pydub import AudioSegment, effects

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
THRESHOLD = 500

class Recorder:
    def __init__(self, fileName):
        self.fileName = '{}.wav'.format(fileName)
        self.recordingThread = None
        #self.frames = array('h')
        self.frames = []
        self.stream = None
        self.audio = None
        self.recording = False

    def start_recording(self):
        self.recording = True
        self.audio = pyaudio.PyAudio()

        # start Recording
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
        self.recordingThread = threading.Thread(target=self._record)
        self.recordingThread.start()

    def stop_recording(self):
        self.recording = False
        self.recordingThread.join()

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        #data = self._normalize_frames()
        #data = pack('<' + ('h'*len(data)), *data)
        waveFile = wave.open(self.fileName, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        #waveFile.writeframes(b''.join(self._normalize_frames()))
        #waveFile.writeframes(data)
        waveFile.writeframes(b''.join(self.frames))
        waveFile.close()

        second_of_silence = AudioSegment.silent(duration=1500, frame_rate=RATE)
        wavFile = AudioSegment.from_wav(self.fileName)
        wavFile = effects.normalize(wavFile)
        result = second_of_silence.append(wavFile).append(second_of_silence)
        result.export(self.fileName, format='wav')

    def _record(self):
        while self.recording:
            self.frames.append(self.stream.read(CHUNK))
            #self.frames.extend(array('h', self.stream.read(CHUNK)))

    def _normalize_frames(self, seconds=5):
        #trim
        result = self._trim(self.frames)

        #add silence
        result = self._add_silence(result)

        result = self._normalize(result)

        return result

    def _trim(self, snd_data):
        "Trim the blank spots at the start and end"
        def _trim_data(snd_data):
            snd_started = False
            r = array('h')

            for i in snd_data:
                if not snd_started and abs(i)>THRESHOLD:
                    snd_started = True
                    r.append(i)

                elif snd_started:
                    r.append(i)
            return r

        # Trim to the left
        snd_data = _trim_data(snd_data)

        # Trim to the right
        snd_data.reverse()
        snd_data = _trim_data(snd_data)
        snd_data.reverse()
        return snd_data

    def _add_silence(self, snd_data, seconds=5):
        "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
        r = array('h', [0 for i in xrange(int(seconds*RATE))])
        r.extend(snd_data)
        r.extend([0 for i in xrange(int(seconds*RATE))])
        return r

    def _normalize(self, snd_data):
        "Average the volume out"
        MAXIMUM = 16384
        times = float(MAXIMUM)/max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i*times))
        return r
