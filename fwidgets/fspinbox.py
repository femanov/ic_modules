from aux.Qt import *

class FSpinBox(QtWidgets.QSpinBox):
    done = QtCore.pyqtSignal(int)

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
        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.update()

    def focusOutEvent(self, event):
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.update()
