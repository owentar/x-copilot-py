from XPWidgets import *
from XPWidgetDefs import *
from XPLMDisplay import *
from XPLMGraphics import *
from XPStandardWidgets import *
from XPLMProcessing import *

HEIGHT = 50
MARGIN = 20
TIMER = 8

class Dimensions:
    def __init__(self):
        self.width = self._getScreenWidth() - (2 * MARGIN)
        self.height = HEIGHT
        self.left = MARGIN
        self.top = 80
        self.right = self.left + self.width
        self.bottom = self.top - self.height

    def _getScreenWidth(self):
        width = []
        XPLMGetScreenSize(width, None)
        return int(width[0])

class StatusWidget:
    def __init__(self, plugin):
        self.plugin = plugin
        self.message = None
        self.dimensions = Dimensions()

        self.widgetId = XPCreateWidget(self.dimensions.left, self.dimensions.top, self.dimensions.right, self.dimensions.bottom, 0, 'X-Copilot', 1, 0, xpWidgetClass_MainWindow)
        XPSetWidgetProperty(self.widgetId, xpProperty_MainWindowType,  xpMainWindowStyle_Translucent)
        XPSetWidgetProperty(self.widgetId, xpProperty_MainWindowHasCloseBoxes, 0) # For now until we fix #24

        self.messageWidget = XPCreateWidget(self.dimensions.left, self.dimensions.top-20, self.dimensions.right, self.dimensions.bottom, 1, 'Recording...', 0, self.widgetId, xpWidgetClass_TextField)
        XPSetWidgetProperty(self.messageWidget, xpProperty_TextFieldType, xpTextTranslucent)
        XPSetWidgetProperty(self.messageWidget, xpProperty_Enabled, 0)

        self.timerLoopCB = self.timerLoopCallback
        XPLMRegisterFlightLoopCallback(self.plugin, self.timerLoopCB, 0, 0)

    def show(self, message):
        self.message = message
        XPShowWidget(self.widgetId)
        XPBringRootWidgetToFront(self.widgetId)
        XPSetWidgetDescriptor(self.messageWidget, self.message)
        XPLMSetFlightLoopCallbackInterval(self.plugin, self.timerLoopCB, TIMER, 1, 0)

    def close(self):
        XPDestroyWidget(self.plugin, self.widgetId, 1)
        XPLMUnregisterFlightLoopCallback(self.plugin, self.timerLoopCB, 0)

    def timerLoopCallback(self, elapsedMe, elapsedSim, counter, refcon):
        XPHideWidget(self.widgetId)
        return 0
