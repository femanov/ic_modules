from aux.Qt import QtCore, QtWidgets

class FCheckBox(QtWidgets.QCheckBox):

    done = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super(FCheckBox, self).__init__(parent)
        self.clicked.connect(self.done)

    def setValue(self, state):
        self.setChecked(state)

    def value(self):
        return self.isChecked()
