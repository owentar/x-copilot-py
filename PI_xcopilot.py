from XPLMDataAccess import *
from XPLMUtilities  import *
from XPLMPlugin     import *
from XPLMDefs       import *
from xcopilot import Recognizer, parseCommand
from xcopilot.xplane import Window
import speech_recognition as sr
import threading

class PythonInterface:
    def XPluginStart(self):
        self.Name = "X-Copilot"
        self.Sig = "Owentar.X-Copilot"
        self.Desc = "A voice commanded copilot"
        self.window = Window(self)

        self.command = XPLMCreateCommand("owentar/xcopilot/record_voice_command", "Record voice command.")
        self.recordVoiceCB = self.recordVoiceCallback
        self.recordVoiceCD = XPLMRegisterCommandHandler(self, self.command, self.recordVoiceCB, 0, 0)

        return self.Name, self.Sig, self.Desc

    def XPluginStop(self):
        XPLMUnregisterCommandHandler(self, self.command, self.recordVoiceCB, 0, 0)
        self.window.close()
        pass

    def XPluginEnable(self):
        return 1

    def XPluginDisable(self):
        pass

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
        pass

    def recordVoiceCallback(self, inCommand, inPhase, inRefcon):
        if inPhase == 0:
            self.recorderThread = threading.Thread(target=self.recordVoice)
            self.recorderThread.start()
        return 0

    def recordVoice(self):
        self.window.show('Recording...')
        r = Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)

        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            strCommand = r.recognize_sphinx2(audio)
            self.window.show('Recorded: ' + strCommand)
            command = parseCommand(strCommand)
            if command is None:
                self.window.show('Recorded: ' + strCommand + ' --> Command unrecognized: ' + strCommand)
            else:
                self.window.show('Command recognized: ' + command.name + ':' + str(command.value))
                for name, value in command.dataRefs.iteritems():
                    dataRef = XPLMFindDataRef(name)
                    XPLMSetDataf(dataRef, value)
        except sr.UnknownValueError:
            self.window.show('Sphinx Speech Recognition could not understand audio')
        except sr.RequestError as e:
            self.window.show('Could not request results from Google Speech Recognition service; {0}'.format(e))
        pass
