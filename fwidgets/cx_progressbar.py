from aQt.QtWidgets import QProgressBar
import pycx4.qcda as cda


class CXProgressBar(QProgressBar):
    def __init__(self, *args, **kwargs):
        super(CXProgressBar, self).__init__(*args)
        self._cname = kwargs.get('cname', None)
        self.chan = None
        self.cx_connect()

    def cx_connect(self):
        if self._cname is None:
            return
        self.chan = cda.IChan(self._cname, private=True, on_update=True)
        self.chan.valueChanged.connect(self.cs_update)

    def cs_update(self, chan):
        if self.value() != chan.val:
            self.setValue(chan.val)

