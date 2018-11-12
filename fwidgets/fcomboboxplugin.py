from aux.Qt import QtGui, QtDesigner
from fwidgets.fcombobox import FComboBox
 
class FComboBoxWidgetPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent=None):
        super().__init__(parent)
 
    def name(self):
        return 'FComboBox'
 
    def group(self):
        return 'CX custom widgets'
 
    def icon(self):
        return QtGui.QIcon()
 
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