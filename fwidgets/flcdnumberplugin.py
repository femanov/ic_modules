from aQt.QtDesigner import QPyDesignerCustomWidgetPlugin
from aQt.QtGui import QIcon
from flcdnumber import FLCDNumber, CXLCDNumber

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
        return 'CXLCDNumber'

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
        return CXLCDNumber(parent)