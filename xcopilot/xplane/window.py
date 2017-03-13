from XPLMDisplay import *
from XPLMGraphics import *

HEIGHT = 80
MARGIN = 20

class Window:

    def __init__(self, plugin):
        self.plugin = plugin
        self.isVisible = 0
        self.message = None
        self.width = self._getScreenWidth() - (2 * MARGIN)

        self.drawWindowCB = self.drawWindowCallback
        self.windowId = XPLMCreateWindow(self.plugin, MARGIN, 100, MARGIN + self.width, 100 - HEIGHT, self.isVisible, self.drawWindowCB, 0, 0, 0)

    def show(self, message):
        self.isVisible = 1
        self.message = message
        XPLMSetWindowIsVisible(self.windowId, self.isVisible)
        XPLMBringWindowToFront(self.windowId)

    def drawWindowCallback(self, inWindowID, inRefcon):
        lLeft = []; lTop = []; lRight = []; lBottom = []
        XPLMGetWindowGeometry(inWindowID, lLeft, lTop, lRight, lBottom)
        left = int(lLeft[0]); top = int(lTop[0]); right = int(lRight[0]); bottom = int(lBottom[0])
        gResult = XPLMDrawTranslucentDarkBox(left, top, right, bottom)
        colour = 1.0, 1.0, 1.0
        if self.message:
            gResult = XPLMDrawString(colour, left + 5, top - 20, self.message, 0, xplmFont_Basic)
        pass

    def close(self):
        XPLMDestroyWindow(self.plugin, self.windowId)

    def _getScreenWidth(self):
        width = []
        XPLMGetScreenSize(width, None)
        return int(width[0])
