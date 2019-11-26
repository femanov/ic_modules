from cxwidgets.aQt.QtWidgets import QCheckBox
from cxwidgets.aQt.QtCore import pyqtSlot, pyqtProperty, pyqtSignal


class FCheckBox(QCheckBox):
    done = pyqtSignal(bool)
    value = pyqtProperty(bool, QCheckBox.isChecked)

    def __init__(self, parent=None, **kwargs):
        super(FCheckBox, self).__init__(parent)
        self.clicked.connect(self.done)

    @pyqtSlot(bool)
    def setValue(self, state):
        self.setChecked(state)
