from aux.Qt import QtGui, QtDesigner
from fwidgets.fdoublespinboxcx import FDoubleSpinBoxCX


class FDoubleSpinBoxCXWidgetPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent=None):
        super(FDoubleSpinBoxCXWidgetPlugin, self).__init__(parent)

    def name(self):
        return 'FDoubleSpinBoxCX'

    def group(self):
        return 'Fedor'

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
        return FDoubleSpinBoxCX(parent)
