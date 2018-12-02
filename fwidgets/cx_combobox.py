from aQt.QtWidgets import QComboBox
from aQt.QtGui import QIcon
from aQt.QtCore import pyqtSlot, pyqtProperty
import pycx4.qcda as cda


class CXTextComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super(CXTextComboBox, self).__init__(*args)
        self._cname = kwargs.get('cname', None)
        self._values = ['none'] + kwargs.get('values', [])
        self._icons = kwargs.get('icons', None)

        self.chan = None
        self.cx_connect()

        for x in range(len(self._values)):
            self.insertItem(x, self._values[x])
            if self._icons is not None and x > 0:
                self.setItemIcon(x, QIcon(self._icons[x-1]))

        self.model().item(0).setEnabled(False)
        # keep next after all
        self.currentIndexChanged.connect(self.cs_send)

    def cx_connect(self):
        if self._cname is None:
            return
        self.chan = cda.StrChan(self._cname, private=True)
        self.chan.valueChanged.connect(self.cs_update)

    @pyqtSlot(str)
    def setValue(self, value):
        try:
            self.setCurrentIndex(self._values.index(value))
        except ValueError:
            self.setCurrentIndex(0)

    def value(self):
        return self._values[self.currentIndex()]

    @pyqtSlot(int)
    def cs_send(self, ind):
        if self.chan.val != self._values[ind]:
            self.chan.setValue(self._values[ind])

    def cs_update(self, chan):
        if self.value() != chan.val:
            self.setValue(chan.val)

    @pyqtSlot(str)
    def set_cname(self, cname):
        self._cname = cname
        self.cx_connect()

    def get_cname(self):
        return self._cname

    cname = pyqtProperty(str, get_cname, set_cname)
