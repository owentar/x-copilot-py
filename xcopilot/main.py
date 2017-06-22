import speech_recognition as sr
from xcopilot.commands import CommandProcessor
from xcopilot.recognizer import Recognizer
from xcopilot.config import ConfigProvider
import logging

class XCopilot:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.commandProcessor = CommandProcessor()
        self.configProvider = ConfigProvider()
        self.recognizer = Recognizer()

    def configureForAircraft(self, aircraftId=('', '', '')):
        config = self.configProvider.get(aircraftId)
        self.commandProcessor.setConfig(config)

    def recordCommand(self):
        with self.getMicrophone() as source:
            audio = self.recognizer.listen(source)
        try:
            strCommand = self.recognizer.recognize_sphinx2(audio)
            command = self.commandProcessor.parseCommand(strCommand)
            if command is None:
                self.logger.info('Command not recognized: %s', strCommand)
                return None
            else:
                self.logger.info('Command recognized: %s:%s', command.name, command.value)
                return command
        except sr.UnknownValueError:
            self.logger.error('Sphinx Speech Recognition could not understand audio')
        except sr.RequestError as e:
            self.logger.error('Could not request results from Google Speech Recognition service; {0}'.format(e))

    def bootstrap(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, 2)
                # audio = self.recognizer.listen(source, 2)
                # capture = self.recognizer.recognize_sphinx2(audio)
                self.logger.info('X-Copilot initialized ({0})'.format(capture))
        except sr.WaitTimeoutError as e:
            self.logger.info('X-Copilot initialized')
        except sr.RequestError as e:
            self.logger.error('Sphinx error; {0}'.format(e))

    def getMicrophone(self):
        return sr.Microphone()
