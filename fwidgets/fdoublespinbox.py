from aux.Qt import *

# class SpinWheelEventFilter(QObject):
#     def eventFilter(self, receiver, event):
#         if event.type() == QEvent.Wheel and receiver.focusPolicy() == Qt.WheelFocus:
#             event.accept()
#             return False
#         else:
#             event.ignore()
#             return True
#         #Call Base Class Method to Continue Normal Event Processing
#         #return super(MyEventFilter,self).eventFilter(receiver, event)


class FDoubleSpinBox(QtWidgets.QDoubleSpinBox):
    done = QtCore.pyqtSignal(float)

    def __init__(self, parent=None):
        super(FDoubleSpinBox, self).__init__(parent)
        self.valueChanged.connect(self.done)
        self.setMinimum(-100000.0)
        self.setMaximum(100000.0)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def wheelEvent(self, event):
        if self.hasFocus():
            super(FDoubleSpinBox, self).wheelEvent(event)
        else:
            event.ignore()

    def focusInEvent(self, event):
        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.update()

    def focusOutEvent(self, event):
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.update()
