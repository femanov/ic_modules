from aQt.QtDesigner import QPyDesignerCustomWidgetCollectionPlugin


from . import fcheckbox
from . import fdoublespinbox
from . import fcombobox

FCheckBox = fcheckbox.FCheckBox
FDoubleSpinBox = fdoublespinbox.FDoubleSpinBox
FComboBox = fcombobox.FComboBox


class CXPlugins(QPyDesignerCustomWidgetCollectionPlugin):
    def __init__(self, parent=None):
        super(CXPlugins, self).__init__(parent)


