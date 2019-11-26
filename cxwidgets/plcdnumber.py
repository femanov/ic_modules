from cxwidgets.aQt.QtWidgets import QLCDNumber
#from aQt.QtCore import *


class FLCDNumber(QLCDNumber):
    def __init__(self, parent=None):
        super(FLCDNumber, self).__init__(parent)



class CXLCDNumber(FLCDNumber):
    pass
