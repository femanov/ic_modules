from aQt.QtWidgets import QLineEdit
import pycx4.qcda as cda

class CXLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super(CXLineEdit, self).__init__(*args)
        self._cname = kwargs.get('cname', None)
        self._max_len = kwargs.get('max_len', 100)
        self.setReadOnly(bool(kwargs.get('readonly', False)))
        self.chan = None
        self.cx_connect()

    def cx_connect(self):
        if self._cname is None:
            return
        self.chan = cda.StrChan(self._cname, max_nelems=self._max_len, private=True, on_update=True)
        self.chan.valueChanged.connect(self.cs_update)

    def cs_update(self, chan):
        if self.text() != chan.val:
            self.setText(chan.val)

    def set_cname(self, cname):
        pass

    def get_cname(self):
        pass

    def set_max_len(self):
        pass

    def get_max_len(self):
        pass