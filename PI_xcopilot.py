from XPLMDataAccess import *
from XPLMUtilities  import *
from XPLMPlugin     import *
from XPLMDefs       import *
from XPLMProcessing import *
from xcopilot import XCopilot
from xcopilot.xplane import StatusWidget
import Queue
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
        self.commandsQueue = Queue.Queue()
        self.isRecording = False
        self.window = StatusWidget(self)
        self.xcopilot = XCopilot()
        self._configureForAircraft()

        self.command = XPLMCreateCommand("xcopilot/record_voice_command", "Record voice command.")
        self.recordVoiceCB = self.recordVoiceCallback
        self.recordVoiceCD = XPLMRegisterCommandHandler(self, self.command, self.recordVoiceCB, 0, 0)

        self.loopCB = self.loopCallback
        XPLMRegisterFlightLoopCallback(self, self.loopCB, 1, 0)

        self.bootstrapThread = threading.Thread(target=self.bootstrap)
        self.bootstrapThread.start()

        return self.Name, self.Sig, self.Desc

    def XPluginStop(self):
        XPLMUnregisterFlightLoopCallback(self, self.loopCB, 0)
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
        if not self.isRecording:
            self.isRecording = True
            self.window.show('Recording...')
            command = self.xcopilot.recordCommand()
            if command is not None:
                self.commandsQueue.put(command)
            else:
                self.window.show('Command not recognized')
            self.isRecording = False

    def loopCallback(self, elapsedMe, elapsedSim, counter, refcon):
        try:
            command = self.commandsQueue.get_nowait()
            self.window.show('Command recognized: {} {}'.format(command.name, command.value))
            if command.command:
                command.command(command.value)
            else:
                for dataRef in command.dataRefs:
                    dataRefID = XPLMFindDataRef(dataRef['name'])
                    SetDataRef[dataRef['type']](dataRefID, command.value)
            self.commandsQueue.task_done()
        except Queue.Empty:
            pass
        return 1

    def bootstrap(self):
        self.xcopilot.bootstrap()

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
