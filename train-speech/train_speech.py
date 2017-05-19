from recorder import Recorder
import os
import uuid
from train_commands_metadata import TRAIN_COMMANDS_METADATA

TRAINING_SPEECH_DIR = os.path.dirname(os.path.abspath(__file__))
TRAINING_SPEECH_DATA_DIR = os.path.join(TRAINING_SPEECH_DIR, 'data')

MENU_OPTIONS = []
MENU_OPTIONS.append('EXIT')
for key in TRAIN_COMMANDS_METADATA:
    MENU_OPTIONS.append(key)

def clear_console():
    os.system('cls' if os.name=='nt' else 'clear')

def setup_directories():
    if not os.path.exists(TRAINING_SPEECH_DATA_DIR):
        os.mkdir(TRAINING_SPEECH_DATA_DIR)

def train_command(command, transcriptions, fileIds):
    commandTrainingMetadata = TRAIN_COMMANDS_METADATA[command]
    for i in commandTrainingMetadata.get('range'):
        wavFileName = '{}'.format(uuid.uuid1())
        transcription = commandTrainingMetadata.get('transcription')(i)
        recorder = Recorder(os.path.join(TRAINING_SPEECH_DATA_DIR, wavFileName))
        raw_input('Command to say: {} (press Enter to start recording)'.format(transcription))
        print 'Recording...'
        recorder.start_recording()
        try:
            raw_input('Press Enter to stop recording')
            recorder.stop_recording()
            transcriptions.write('<s> {} </s> ({})\n'.format(transcription, wavFileName))
            fileIds.write('{}\n'.format(wavFileName))
        except KeyboardInterrupt:
            print 'Ignoring this recording'
            recorder.stop_recording(save=False)

def show_menu():
    print 40 * '='
    print 'Train Commands Speech Recognition Menu:'
    print 40 * '-'
    for idx, command in enumerate(MENU_OPTIONS[1:]):
        print '{}. {}'.format(idx + 1, command)
    print 40 * '-'
    print '0. EXIT'
    print 40 * '='
    try:
        return int(raw_input('Choose an option number and press Enter: '))
    except ValueError, e :
        clear_console()
        print 'Invalid option, please inidcate the option number and press Enter'
        return show_menu()

def main():
    setup_directories()

    transcriptions = open(os.path.join(TRAINING_SPEECH_DATA_DIR, 'train-speech.transcription'), 'a')
    fileIds = open(os.path.join(TRAINING_SPEECH_DATA_DIR, 'train-speech.fileids'), 'a')

    menuOption = show_menu()
    while (menuOption):
        if (menuOption == 0):
            break
        elif (len(MENU_OPTIONS) > menuOption):
            train_command(MENU_OPTIONS[menuOption], transcriptions, fileIds)
        clear_console()
        menuOption = show_menu()

    transcriptions.close()
    fileIds.close()

main()
