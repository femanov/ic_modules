from aux.Qt import QtGui, QtDesigner
from fwidgets.doublespinboxcx import DoubleSpinBoxCX


class DoubleSpinBoxCXWidgetPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent=None):
        super(DoubleSpinBoxCXWidgetPlugin, self).__init__(parent)

    def name(self):
        return 'DoubleSpinBoxCX'

    def group(self):
        return 'CX widgets'

    def icon(self):
        return QtGui.QIcon()

    def isContainer(self):
        return False

    def includeFile(self):
        return 'fwidgets.fdoublespinboxcx'

    def toolTip(self):
        return 'a double spinbox adapted to CX control system'

    def whatsThis(self):
        return 'a double spinbox adapted to CX control system'

    def createWidget(self, parent):
        return DoubleSpinBoxCX(parent)
