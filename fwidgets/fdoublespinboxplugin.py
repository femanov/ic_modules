from aux.Qt import *
from fdoublespinbox import *


class FDoubleSpinBoxWidgetPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent=None):
        super().__init__(parent)
 
    def name(self):
        return 'FDoubleSpinBox'
 
    def group(self):
        return 'Fedor'
 
    def icon(self):
        return QtGui.QIcon()
 
    def isContainer(self):
        return False
 
    def includeFile(self):
        return 'fwidgets.fdoublespinbox'
 
    def toolTip(self):
        return 'a double spinbox adapted to BINP IC control system'
 
    def whatsThis(self):
        return 'a double spinbox adapted to BINP IC control system'
 
    def createWidget(self, parent):
        return FDoubleSpinBox(parent)
