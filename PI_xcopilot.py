from XPLMDisplay import *
from XPLMGraphics import *
from XPLMDataAccess import *
from XPLMUtilities  import *
from XPLMPlugin     import *
from XPLMDefs       import *
from xcopilot import Recognizer, parseCommand
import speech_recognition as sr
import threading

class PythonInterface:
    def XPluginStart(self):
        self.Name = "X-Copilot"
        self.Sig = "Owentar.X-Copilot"
        self.Desc = "A voice commanded copilot"
        self.message = "Initialized"

        self.command = XPLMCreateCommand("owentar/xcopilot/record_voice_command", "Record voice command.")
        self.recordVoiceCB = self.recordVoiceCallback
        self.recordVoiceCD = XPLMRegisterCommandHandler(self, self.command, self.recordVoiceCB, 0, 0)

        self.drawWindowCB = self.drawWindowCallback
        self.windowId = XPLMCreateWindow(self, 50, 600, 300, 400, 1, self.drawWindowCB, 0, 0, 0)

        return self.Name, self.Sig, self.Desc

    def XPluginStop(self):
        XPLMUnregisterCommandHandler(self, self.command, self.recordVoiceCB, 0, 0)
        XPLMDestroyWindow(self, self.windowId)
        pass

    def XPluginEnable(self):
        return 1

    def XPluginDisable(self):
        pass

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
        pass

    def drawWindowCallback(self, inWindowID, inRefcon):
        lLeft = []; lTop = []; lRight = []; lBottom = []
        XPLMGetWindowGeometry(inWindowID, lLeft, lTop, lRight, lBottom)
        left = int(lLeft[0]); top = int(lTop[0]); right = int(lRight[0]); bottom = int(lBottom[0])
        gResult = XPLMDrawTranslucentDarkBox(left, top, right, bottom)
        colour = 1.0, 1.0, 1.0
        if self.message:
            gResult = XPLMDrawString(colour, left + 5, top - 20, self.message, 0, xplmFont_Basic)
        pass

    def recordVoiceCallback(self, inCommand, inPhase, inRefcon):
        if inPhase == 0:
            self.recorderThread = threading.Thread(target=self.recordVoice)
            self.recorderThread.start()
        return 0

    def recordVoice(self):
        self.message = "Recording"
        r = Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)

        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            strCommand = r.recognize_sphinx2(audio)
            self.message = "Recorded: " + strCommand
            command = parseCommand(strCommand)
            if command is None:
                self.message = self.message + " --> Command unrecognized: " + strCommand
            else:
                self.message = "Command recognized: " + command.name + ":" + str(command.dataRefs["sim/cockpit2/gauges/actuators/barometer_setting_in_hg_pilot"])
                for name, value in command.dataRefs.iteritems():
                    dataRef = XPLMFindDataRef(name)
                    XPLMSetDataf(dataRef, value)
        except sr.UnknownValueError:
            self.message = "Sphinx Speech Recognition could not understand audio"
        except sr.RequestError as e:
            self.message = "Could not request results from Google Speech Recognition service; {0}".format(e)
        pass
