from aux.Qt import QtCore, QtWidgets
from fcheckbox import FCheckBox
import pycx4.qcda as cda


class CXCheckBox(FCheckBox):
    def __init__(self, parent=None, **kwargs):
        super(CXCheckBox, self).__init__()
        if 'cname' in kwargs:
            self._cname = kwargs['cname']
        else:
            self._cname = None

        self.chan = None
        self.cx_connect()
        self.done.connect(self.cs_send)

    def cx_connect(self):
        if self._cname is None:
            return
        self.chan = cda.DChan(self._cname, private=True)
        self.chan.valueChanged.connect(self.cs_update)

    @QtCore.pyqtSlot(bool)
    def cs_send(self, value):
        self.chan.setValue(value)

    def cs_update(self, chan):
        if chan.val != 0:
            self.setValue(QtCore.Qt.Checked)
        else:
            self.setValue(QtCore.Qt.Unchecked)

    @QtCore.pyqtSlot(str)
    def set_cname(self, cname):
        self._cname = cname
        self.cx_connect()

    def get_cname(self):
        return self._cname

    cname = QtCore.pyqtProperty(str, get_cname, set_cname)



