from aux.Qt import *
from fspinbox import *


class FSpinBoxWidgetPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent=None):
        super().__init__(parent)
 
    def name(self):
        return 'FSpinBox'
 
    def group(self):
        return 'CX custom widgets'
 
    def icon(self):
        return QtGui.QIcon()
 
    def isContainer(self):
        return False
 
    def includeFile(self):
        return 'fwidgets.fspinbox'
 
    def toolTip(self):
        return 'a spinbox adapted to BINP IC control system'
 
    def whatsThis(self):
        return 'a spinbox adapted to BINP IC control system'
 
    def createWidget(self, parent):
        return FSpinBox(parent)