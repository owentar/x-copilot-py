from XPLMDataAccess import *
from XPLMUtilities  import *
from XPLMPlugin     import *
from XPLMDefs       import *
from xcopilot import XCopilot
from xcopilot.xplane import StatusWidget
import speech_recognition as sr
import threading
import os
import logging

XPLM_MSG_PLANE_LOADED = 102

SetDataRef = {
    'float': XPLMSetDataf,
    'int': XPLMSetDatai,
    'boolean': XPLMSetDatai,
    'double': XPLMSetDatad
}

class PythonInterface:
    def XPluginStart(self):
        logging.basicConfig(filename=os.sep.join(['Resources', 'plugins', 'PythonScripts', 'xcopilot', 'xcopilot.log']), filemode='w', level=logging.DEBUG)
        self.Name = "X-Copilot"
        self.Sig = "Owentar.X-Copilot"
        self.Desc = "A voice commanded copilot"
        self.window = StatusWidget(self)
        self.xcopilot = XCopilot()
        self._configureForAircraft()

        self.command = XPLMCreateCommand("owentar/xcopilot/record_voice_command", "Record voice command.")
        self.recordVoiceCB = self.recordVoiceCallback
        self.recordVoiceCD = XPLMRegisterCommandHandler(self, self.command, self.recordVoiceCB, 0, 0)

        return self.Name, self.Sig, self.Desc

    def XPluginStop(self):
        XPLMUnregisterCommandHandler(self, self.command, self.recordVoiceCB, 0, 0)
        self.window.close()

    def XPluginEnable(self):
        return 1

    def XPluginDisable(self):
        pass

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
        if inMessage == XPLM_MSG_PLANE_LOADED:
            self._configureForAircraft()

    def recordVoiceCallback(self, inCommand, inPhase, inRefcon):
        if inPhase == 0:
            self.recorderThread = threading.Thread(target=self.recordVoice)
            self.recorderThread.start()
        return 0

    def recordVoice(self):
        self.window.show('Recording...')
        result = self.xcopilot.recordCommand()
        if result is not None:
            command = result[0]
            self.window.show('Command recognized: {} {}'.format(command.name, command.value))
            dataRefs = result[1]
            for dataRef in dataRefs:
                dataRefID = XPLMFindDataRef(dataRef['name'])
                SetDataRef[dataRef['type']](dataRefID, command.value)
        else:
            self.window.show('Command not recognized')

    def _configureForAircraft(self):
        authorID = XPLMFindDataRef('sim/aircraft/view/acf_author')
        ICAOID = XPLMFindDataRef('sim/aircraft/view/acf_ICAO')
        descID = XPLMFindDataRef('sim/aircraft/view/acf_descrip')
        author = []
        icao = []
        desc = []
        XPLMGetDatab(authorID, author, 0, 500)
        XPLMGetDatab(ICAOID, icao, 0, 40)
        XPLMGetDatab(descID, desc, 0, 260)
        self.xcopilot.configureForAircraft((str(author[0]), str(desc[0]), str(icao[0])))
