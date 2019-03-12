from aQt.QtCore import pyqtSlot, pyqtProperty, Qt
from .fcheckbox import FCheckBox
import pycx4.qcda as cda


class CXCheckBox(FCheckBox):
    def __init__(self, parent=None, **kwargs):
        super(CXCheckBox, self).__init__(parent, **kwargs)
        self._cname = kwargs.get('cname', None)
        self.chan = None
        self.cx_connect()
        self.done.connect(self.cs_send)

    def cx_connect(self):
        if self._cname is None:
            return
        self.chan = cda.IChan(self._cname, private=True)
        self.chan.valueChanged.connect(self.cs_update)

    @pyqtSlot(bool)
    def cs_send(self, value):
        if int(value) == self.chan.val:
            return
        self.chan.setValue(value)

    def cs_update(self, chan):
        if chan.val != 0:
            self.setValue(Qt.Checked)
        else:
            self.setValue(Qt.Unchecked)

    @pyqtSlot(str)
    def set_cname(self, cname):
        if self._cname == cname:
            return
        self._cname = cname
        self.cx_connect()

    def get_cname(self):
        return self._cname

    cname = pyqtProperty(str, get_cname, set_cname)



