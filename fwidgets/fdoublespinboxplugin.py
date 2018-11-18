from aQt.QtDesigner import QPyDesignerCustomWidgetPlugin
from aQt.QtGui import QIcon
from fdoublespinbox import FDoubleSpinBox


class FDoubleSpinBoxWidgetPlugin(QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent=None):
        super().__init__(parent)
 
    def name(self):
        return 'FDoubleSpinBox'
 
    def group(self):
        return 'CX custom widgets'
 
    def icon(self):
        return QIcon()
 
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
