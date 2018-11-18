from aQt.QtDesigner import QPyDesignerCustomWidgetPlugin
from aQt.QtGui import QIcon

from fcheckbox import FCheckBox
 
class FComboBoxWidgetPlugin(QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent=None):
        super(FComboBoxWidgetPlugin, self).__init__(parent)
 
    def name(self):
        return 'FCheckBox'
 
    def group(self):
        return 'CX custom widgets'
 
    def icon(self):
        return QIcon()
 
    def isContainer(self):
        return False
 
    def includeFile(self):
        return 'fwidgets.fcheckbox'
 
    def toolTip(self):
        return 'a combobox adapted to BINP IC control system'
 
    def whatsThis(self):
        return 'a combobox adapted to BINP IC control system'
 
    def createWidget(self, parent):
        return FCheckBox(parent)
