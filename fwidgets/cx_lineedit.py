from aQt.QtWidrets import QLineEdit



class CXLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super(CXLineEdit, self).__init__(*args)
        self._cname = kwargs.get('cname', None)

