import speech_recognition as sr
from xcopilot.commands import CommandProcessor
from xcopilot.recognizer import Recognizer
from xcopilot.config.dataref import DataRefProvider

class XCopilot:
    def __init__(self):
        self.commandProcessor = CommandProcessor()
        self.dataRefProvider = DataRefProvider()
        self.recognizer = Recognizer()

    def configureForAircraft(self, aircraftId):
        self.dataRef = self.dataRefProvider.get(aircraftId)

    def recordCommand(self):
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)

        try:
            strCommand = self.recognizer.recognize_sphinx2(audio)
            print 'Recorded: ' + strCommand
            command = self.commandProcessor.parseCommand(strCommand)
            if command is None:
                print 'Recorded: ' + strCommand + ' --> Command unrecognized: ' + strCommand
            else:
                print 'Command recognized: ' + command.name + ':' + str(command.value)
                commandDataRefs = self.dataRef.get(command.name)
                return (command, commandDataRefs)
        except sr.UnknownValueError:
            print 'Sphinx Speech Recognition could not understand audio'
        except sr.RequestError as e:
            print 'Could not request results from Google Speech Recognition service; {0}'.format(e)
