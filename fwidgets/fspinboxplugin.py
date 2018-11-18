from aQt.QtDesigner import QPyDesignerCustomWidgetPlugin
from aQt.QtGui import QIcon
from fspinbox import FSpinBox


class FSpinBoxWidgetPlugin(QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent=None):
        super().__init__(parent)
 
    def name(self):
        return 'FSpinBox'
 
    def group(self):
        return 'CX custom widgets'
 
    def icon(self):
        return QIcon()
 
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
