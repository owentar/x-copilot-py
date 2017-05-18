from recorder import Recorder
from os import mkdir, path
from shutil import rmtree

TO_NUMBER = {
    0: 'ZERO',
    1: 'ONE',
    2: 'TWO',
    3: 'THREE',
    4: 'FOUR',
    5: 'FIVE',
    6: 'SIX',
    7: 'SEVEN',
    8: 'EIGHT',
    9: 'NINE'
}

TRAINING_SPEECH_DIR = path.dirname(path.abspath(__file__))
TRAINING_SPEECH_DATA_DIR = path.join(TRAINING_SPEECH_DIR, 'data')

def setup_directories():
    if path.exists(TRAINING_SPEECH_DATA_DIR):
        print 'Deleting previous training data'
        rmtree(TRAINING_SPEECH_DATA_DIR)

    mkdir(TRAINING_SPEECH_DATA_DIR)

setup_directories()

transcriptions = open(path.join(TRAINING_SPEECH_DATA_DIR, 'train-speech.transcription'), 'w')
fileIds = open(path.join(TRAINING_SPEECH_DATA_DIR, 'train-speech.fileids'), 'w')

for i in range(0, 10):
    wavFileName = 'SET_ALTIMETER_299{}'.format(i)
    number = TO_NUMBER[i]
    transcription = 'SET ALTIMETER TWO NINE NINE {}'.format(number)
    recorder = Recorder(path.join(TRAINING_SPEECH_DATA_DIR, wavFileName))
    raw_input('Command to say: {} (press Enter to start recording)'.format(transcription))
    print 'Recording...'
    recorder.start_recording()
    raw_input('Press Enter to stop recording')
    recorder.stop_recording()
    transcriptions.write('<s> {} </s> ({})\n'.format(transcription, wavFileName))
    fileIds.write('{}\n'.format(wavFileName))

transcriptions.close()
fileIds.close()
print 'Done!'
#print "recording..."
#start_recording()
#raw_input('recording... (press Enter to stop recording)')
#stop_recording()
#print "Done!"
