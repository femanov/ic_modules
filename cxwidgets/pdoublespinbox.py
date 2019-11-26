from cxwidgets.aQt.QtCore import Qt, pyqtSignal
from cxwidgets.aQt.QtWidgets import QDoubleSpinBox


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


class FDoubleSpinBox(QDoubleSpinBox):
    done = pyqtSignal(float)

    def __init__(self, parent=None, **kwargs):
        super(FDoubleSpinBox, self).__init__(parent)
        self.valueChanged.connect(self.done)
        self.setMinimum(kwargs.get('min', -100000.0))
        self.setMaximum(kwargs.get('max', 100000.0))

        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, event):
        if self.hasFocus():
            super(FDoubleSpinBox, self).wheelEvent(event)
        else:
            event.ignore()

    def focusInEvent(self, event):
        self.setFocusPolicy(Qt.WheelFocus)
        self.update()

    def focusOutEvent(self, event):
        self.setFocusPolicy(Qt.StrongFocus)
        self.update()
