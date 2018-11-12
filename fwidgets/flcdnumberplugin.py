from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin
from PyQt5.QtGui import QIcon
from flcdnumber import *

class FLCDNumberWidgetPlugin(QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent=None):
        super().__init__(parent)
 
    def name(self):
        return 'FLCDNumber'
 
    def group(self):
        return 'CX custom widgets'
 
    def icon(self):
        return QIcon()
 
    def isContainer(self):
        return False
 
    def includeFile(self):
        return 'fwidgets.flcdnumber'
 
    def toolTip(self):
        return 'a LCDNumber adapted to BINP IC control system'
 
    def whatsThis(self):
        return 'a LCDNumber adapted to BINP IC control system'
 
    def createWidget(self, parent):
        return FLCDNumber(parent)


class FLCDNumberCXWidgetPlugin(QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent=None):
        QPyDesignerCustomWidgetPlugin.__init__(self)

    def name(self):
        return 'FLCDNumberCX'

    def group(self):
        return 'Fedor'

    def icon(self):
        return QIcon()

    def isContainer(self):
        return False

    def includeFile(self):
        return 'fwidgets.flcdnumber'

    def toolTip(self):
        return 'a LCDNumber adapted to BINP IC control system'

    def whatsThis(self):
        return 'a LCDNumber adapted to BINP IC control system'

    def createWidget(self, parent):
        return FLCDNumberCX(parent)