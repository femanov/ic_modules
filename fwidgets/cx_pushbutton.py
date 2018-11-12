from aux.Qt import QtCore, QtWidgets
import pycx4.qcda as cda


class CXPushButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super(CXPushButton, self).__init__(*args, **kwargs)
        self._cname = kwargs.get('cname', None)
        self.chan = None
        self.cx_connect()
        self.clicked.connect(self.cs_send)

    def cx_connect(self):
        if self._cname is None:
            return
        self.chan = cda.DChan(self._cname, private=True)

    @QtCore.pyqtSlot()
    def cs_send(self):
        self.chan.setValue(1)

    @QtCore.pyqtSlot(str)
    def set_cname(self, cname):
        self._cname = cname
        self.cx_connect()

    def get_cname(self):
        return self._cname

    cname = QtCore.pyqtProperty(str, get_cname, set_cname)



