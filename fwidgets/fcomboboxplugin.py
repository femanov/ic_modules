#import os
#modpath = os.path.dirname(os.path.realpath(__file__))


from aQt.QtGui import QIcon
from aQt.QtDesigner import QPyDesignerCustomWidgetPlugin
from fwidgets.fcombobox import FComboBox
 
class FComboBoxWidgetPlugin(QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent=None):
        super(FComboBoxWidgetPlugin, self).__init__(parent)
 
    def name(self):
        return 'FComboBox'
 
    def group(self):
        return 'CX custom widgets'
 
    def icon(self):
        return QIcon("./img/icon1.png")
 
    def isContainer(self):
        return False
 
    def includeFile(self):
        return 'fwidgets.fcombobox'

    def toolTip(self):
        return 'a combobox adapted to BINP IC control system'
 
    def whatsThis(self):
        return 'a combobox adapted to BINP IC control system'
 
    def createWidget(self, parent):
        return FComboBox(parent)
