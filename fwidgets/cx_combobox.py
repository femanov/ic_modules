from aux.Qt import QtCore, QtWidgets
import pycx4.qcda as cda


class CXTextComboBox(QtWidgets.QComboBox):
    def __init__(self, *args, **kwargs):
        super(CXTextComboBox, self).__init__(*args,)
        self._cname = kwargs.get('cname', None)
        self._values = kwargs.get('values', None)

        self.chan = None
        self.cx_connect()
        self.currentIndexChanged.connect(self.cs_send)

        for x in range(len(self._values)):
            self.insertItem(x, self._values[x])

    def cx_connect(self):
        if self._cname is None:
            return
        self.chan = cda.StrChan(self._cname, private=True)
        self.chan.valueChanged.connect(self.cs_update)

    def setValue(self, value):
        try:
            self.setCurrentIndex(self._values.index(value))
        except ValueError:
            self.setCurrentIndex(1)

    @QtCore.pyqtSlot(int)
    def cs_send(self, ind):
        self.chan.setValue(self._values[ind])

    def cs_update(self, chan):
        self.setValue(chan.val)

    @QtCore.pyqtSlot(str)
    def set_cname(self, cname):
        self._cname = cname
        self.cx_connect()

    def get_cname(self):
        return self._cname

    cname = QtCore.pyqtProperty(str, get_cname, set_cname)
