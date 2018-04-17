from aux.Qt import QtCore, QtWidgets
import pycx4.qcda as cda


class FDoubleSpinBoxCX(QtWidgets.QDoubleSpinBox):

    done = QtCore.pyqtSignal(float)
    cxname = QtCore.pyqtProperty(str)

    def __init__(self, parent=None):
        super(FDoubleSpinBoxCX, self).__init__(parent)
        self.valueChanged.connect(self.done)
        self.chan = None
        self.cname = "canhw:11.rings.iset"
        #self.cx_connect()

    def cx_connect(self):
        self.chan = cda.DChan(self.cname)
        self.chan.valueChanged.connect(self.renew)

    def renew(self, chan):
        print(chan.val)
        pass
