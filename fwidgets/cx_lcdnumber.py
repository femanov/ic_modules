from aux.Qt import *
import pycx4.qcda as cda


class CXLCDNumber(QtWidgets.QLCDNumber):
    def __init__(self, parent=None, cname=None):
        super(CXLCDNumber, self).__init__(parent)

        self.chan = None
        self._cname = cname
        self.cx_connect()

    def cx_connect(self):
        if self._cname is None:
            return
        self.chan = cda.DChan(self._cname, private=True)
        self.chan.valueChanged.connect(self.cs_update)

    def cs_update(self, chan):
        self.display(chan.val)

    @QtCore.pyqtSlot(float)
    def setCname(self, cname):
        self._cname = cname
        self.cx_connect()

    def getCname(self):
        return self._cname

    cname = QtCore.pyqtProperty(str, getCname, setCname)
