from aQt.QtGui import QColor
from aQt.QtCore import QTimer
import pycx4.qcda as cda
from .ledwidget import LedWidget


class CXEventLed(LedWidget):
    def __init__(self, parent=None, **kwargs):
        super(CXEventLed, self).__init__(parent)

        self._cname = kwargs.get('cname', None)
        self.chan = None
        self.cx_connect()

        self.timer = QTimer()

    def cx_connect(self):
        if self._cname is None:
            return
        self.chan = cda.IChan(self._cname, private=True, on_update=True)
        self.chan.valueMeasured.connect(self.cs_update)

    def cs_update(self, chan):
        self.color = QColor(0, 255, 0)
        self.timer.singleShot(200, self.unlight)

    def unlight(self):
        self.color = QColor(0, 50, 0)




