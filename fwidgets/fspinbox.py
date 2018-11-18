from aQt.QtWidgets import QSpinBox
from aQt.QtCore import pyqtSignal, Qt

class FSpinBox(QSpinBox):
    done = pyqtSignal(int)

    def __init__(self, parent=None):
        super(FSpinBox, self).__init__(parent)
        self.valueChanged.connect(self.done)

        self.setMinimum(-100000)
        self.setMaximum(100000)

    def wheelEvent(self, event):
        if self.hasFocus():
            super(FSpinBox, self).wheelEvent(event)
        else:
            event.ignore()

    def focusInEvent(self, event):
        self.setFocusPolicy(Qt.WheelFocus)
        self.update()

    def focusOutEvent(self, event):
        self.setFocusPolicy(Qt.StrongFocus)
        self.update()
