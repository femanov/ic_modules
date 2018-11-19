from aQt.QtWidgets import QComboBox
from aQt.QtCore import pyqtSlot, pyqtProperty
import pycx4.qcda as cda


class CXTextComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super(CXTextComboBox, self).__init__(*args)
        self._cname = kwargs.get('cname', None)
        self._values = ['None'] + kwargs.get('values', [])


        self.chan = None
        self.cx_connect()
        self.currentIndexChanged.connect(self.cs_send)

        for x in range(len(self._values)):
            self.insertItem(x, self._values[x])

        self.model().item(0).setEnabled(False)

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
        return(self._values[self.currentIndex()])

    @pyqtSlot(int)
    def cs_send(self, ind):
        print("sending")
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
