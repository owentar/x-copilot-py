from XPLMDisplay import *
from XPLMGraphics import *
from XPLMProcessing import *

HEIGHT = 80
MARGIN = 20
TIMER = 8

class Window:

    def __init__(self, plugin):
        self.plugin = plugin
        self.message = None
        self.width = self._getScreenWidth() - (2 * MARGIN)

        self.drawWindowCB = self.drawWindowCallback
        self.windowId = XPLMCreateWindow(self.plugin, MARGIN, 100, MARGIN + self.width, 100 - HEIGHT, 0, self.drawWindowCB, 0, 0, 0)

        self.timerLoopCB = self.timerLoopCallback
        XPLMRegisterFlightLoopCallback(self.plugin, self.timerLoopCB, 0, 0)

    def show(self, message):
        self.message = message
        XPLMSetWindowIsVisible(self.windowId, 1)
        XPLMBringWindowToFront(self.windowId)
        XPLMSetFlightLoopCallbackInterval(self.plugin, self.timerLoopCB, TIMER, 1, 0)

    def drawWindowCallback(self, inWindowID, inRefcon):
        lLeft = []; lTop = []; lRight = []; lBottom = []
        XPLMGetWindowGeometry(inWindowID, lLeft, lTop, lRight, lBottom)
        left = int(lLeft[0]); top = int(lTop[0]); right = int(lRight[0]); bottom = int(lBottom[0])
        gResult = XPLMDrawTranslucentDarkBox(left, top, right, bottom)
        colour = 1.0, 1.0, 1.0
        if self.message:
            gResult = XPLMDrawString(colour, left + 5, top - 20, self.message, 0, xplmFont_Basic)
        pass

    def timerLoopCallback(self, elapsedMe, elapsedSim, counter, refcon):
        XPLMSetWindowIsVisible(self.windowId, 0)
        return 0

    def close(self):
        XPLMDestroyWindow(self.plugin, self.windowId)
        XPLMUnregisterFlightLoopCallback(self.plugin, self.timerLoopCB, 0)

    def _getScreenWidth(self):
        width = []
        XPLMGetScreenSize(width, None)
        return int(width[0])
