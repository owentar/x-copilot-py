from XPLMDataAccess import *
from XPLMUtilities  import *
from XPLMPlugin     import *
from XPLMDefs       import *
from xcopilot import XCopilot
from xcopilot.xplane import Window
import speech_recognition as sr
import threading

XPLM_MSG_PLANE_LOADED = 102

SetDataRef = {
    'float': XPLMSetDataf,
    'int': XPLMSetDatai,
    'boolean': XPLMSetDatai,
    'double': XPLMSetDatad
}

class PythonInterface:
    def XPluginStart(self):
        self.Name = "X-Copilot"
        self.Sig = "Owentar.X-Copilot"
        self.Desc = "A voice commanded copilot"
        self.window = Window(self)
        self.xcopilot = XCopilot()

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
        if inMessage == XPLM_MSG_PLANE_LOADED:
            # TODO: load config for the airplane

    def recordVoiceCallback(self, inCommand, inPhase, inRefcon):
        if inPhase == 0:
            self.recorderThread = threading.Thread(target=self.recordVoice)
            self.recorderThread.start()
        return 0

    def recordVoice(self):
        self.window.show('Recording...')
        result = self.xcopilot.recordCommand()
        command = result[0]
        dataRefs = result[1]
        for dataRef in dataRefs:
            dataRefID = XPLMFindDataRef(dataRef)
            SetDataRef[command.type](dataRefID, command.value)
