from aQt.QtCore import pyqtSlot, pyqtProperty, Qt
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
        if QMouseEvent.button() == Qt.LeftButton:
            print("Left Button Clicked")
        elif QMouseEvent.button() == Qt.RightButton:
            #do what you want here
            print("Right Button Clicked")


    def cx_connect(self):
        if self._cname is None:
            return
        self.chan = cda.IChan(self._cname, private=True)
        self.chan.valueChanged.connect(self.cs_update)

    @pyqtSlot(int)
    def cs_send(self, value):
        if int(value) == self.chan.val:
            return
        self.chan.setValue(value)

    def cs_update(self, chan):
        if int(self.value()) == chan.val:
            return
        self.setValue(chan.val)

    @pyqtSlot(str)
    def set_cname(self, cname):
        if self._cname == cname:
            return
        self._cname = cname
        self.cx_connect()

    def get_cname(self):
        return self._cname

    cname = pyqtProperty(str, get_cname, set_cname)

