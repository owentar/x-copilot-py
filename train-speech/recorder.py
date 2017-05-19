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

    def stop_recording(self, save=True):
        self.recording = False
        self.recordingThread.join()

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        if (save):
            waveFile = wave.open(self.fileName, 'wb')
            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(self.audio.get_sample_size(FORMAT))
            waveFile.setframerate(RATE)
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
