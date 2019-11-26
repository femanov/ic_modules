from cxwidgets.aQt.QtDesigner import QPyDesignerCustomWidgetPlugin
from cxwidgets.aQt.QtGui import QIcon
from cxwidgets import FDoubleSpinBox, FCheckBox, FLCDNumber, FSpinBox, LedWidget


class FDoubleSpinBoxWidgetPlugin(QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent=None):
        super(FDoubleSpinBoxWidgetPlugin, self).__init__(parent)

    def name(self):
        return 'FDoubleSpinBox'

    def group(self):
        return 'polymorph widgets'

    def icon(self):
        return QIcon()

    def isContainer(self):
        return False

    def includeFile(self):
        return 'cxwidgets'

    def toolTip(self):
        return 'a double spinbox from polymorphs'

    def whatsThis(self):
        return 'a double spinbox from polymorphs'

    def createWidget(self, parent):
        return FDoubleSpinBox(parent)


class FComboBoxWidgetPlugin(FDoubleSpinBoxWidgetPlugin):
    def name(self):
        return 'FCheckBox'

    def toolTip(self):
        return 'checkbox from polymorphs'

    def whatsThis(self):
        return 'checkbox from polymorphs'

    def createWidget(self, parent):
        return FCheckBox(parent)


class FLCDNumberWidgetPlugin(FDoubleSpinBoxWidgetPlugin):
    def name(self):
        return 'FLCDNumber'

    def toolTip(self):
        return 'LCDNumber from polymorphs'

    def whatsThis(self):
        return 'LCDNumber from polymorphs'

    def createWidget(self, parent):
        return FLCDNumber(parent)


class FSpinBoxWidgetPlugin(FDoubleSpinBoxWidgetPlugin):
    def name(self):
        return 'FSpinBox'

    def toolTip(self):
        return 'spinbox from polymorphs'

    def whatsThis(self):
        return 'spinbox from polymorphs'

    def createWidget(self, parent):
        return FSpinBox(parent)


class LedPlugin(FDoubleSpinBoxWidgetPlugin):
    def name(self):
        return "LedWidget"

    def toolTip(self):
        return "LED-like"

    def whatsThis(self):
        return "LED-like"

    def createWidget(self, parent):
        return LedWidget(parent)

