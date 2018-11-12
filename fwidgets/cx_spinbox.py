from aux.Qt import QtCore, QtWidgets
import pycx4.qcda as cda
from .fspinbox import FSpinBox


class CXSpinBox(FSpinBox):
    def __init__(self, parent=None, cname=None):
        super(CXSpinBox, self).__init__(parent)
        self.valueChanged.connect(self.done)
        self.chan = None
        self._cname = cname
        self.cx_connect()

        self.done.connect(self.cs_send)


    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == QtCore.Qt.LeftButton:
            print("Left Button Clicked")
        elif QMouseEvent.button() == QtCore.Qt.RightButton:
            #do what you want here
            print("Right Button Clicked")


    def cx_connect(self):
        if self._cname is None:
            return
        self.chan = cda.DChan(self._cname, private=True)
        self.chan.valueChanged.connect(self.cs_update)

    @QtCore.pyqtSlot(int)
    def cs_send(self, value):
        self.chan.setValue(value)

    def cs_update(self, chan):
        self.setValue(chan.val)

    @QtCore.pyqtSlot(str)
    def setCname(self, cname):
        self._cname = cname
        self.cx_connect()

    def getCname(self):
        return self._cname

    cname = QtCore.pyqtProperty(str, getCname, setCname)

