from aux.Qt import QtGui, QtDesigner
from fcheckbox import *
 
class FComboBoxWidgetPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent=None):
        super(FComboBoxWidgetPlugin, self).__init__(parent)
 
    def name(self):
        return 'FCheckBox'
 
    def group(self):
        return 'Fedor'
 
    def icon(self):
        return QtGui.QIcon()
 
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
