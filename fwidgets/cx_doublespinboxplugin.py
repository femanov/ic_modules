from aQt.QtDesigner import QPyDesignerCustomWidgetPlugin
from aQt.QtGui import QIcon
from fwidgets.cx_doublespinbox import CXDoubleSpinBox


class DoubleSpinBoxCXWidgetPlugin(QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent=None):
        super(DoubleSpinBoxCXWidgetPlugin, self).__init__(parent)

    def name(self):
        return 'CXDoubleSpinBox'

    def group(self):
        return 'CX custom widgets'

    def icon(self):
        return QIcon()

    def isContainer(self):
        return False

    def includeFile(self):
        return 'fwidgets.cx_fdoublespinbox'

    def toolTip(self):
        return 'a double spinbox adapted to CX control system'

    def whatsThis(self):
        return 'a double spinbox adapted to CX control system'

    def createWidget(self, parent):
        return CXDoubleSpinBox(parent)
