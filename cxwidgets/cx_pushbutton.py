from cxwidgets.aQt.QtWidgets import QPushButton
from cxwidgets.aQt.QtCore import pyqtSlot, pyqtProperty
import pycx4.qcda as cda


class CXPushButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(CXPushButton, self).__init__(*args, **kwargs)
        self._cname = kwargs.get('cname', None)
        self.chan = None
        self.cx_connect()
        self.clicked.connect(self.cs_send)

    def cx_connect(self):
        if self._cname is None or self._cname == '':
            return
        self.chan = cda.IChan(self._cname, private=True, on_update=True)

    @pyqtSlot()
    def cs_send(self):
        self.chan.setValue(1)

    @pyqtSlot(str)
    def set_cname(self, cname):
        self._cname = cname
        self.cx_connect()

    def get_cname(self):
        return self._cname

    cname = pyqtProperty(str, get_cname, set_cname)



