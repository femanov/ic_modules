from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#from actl import *

class FLCDNumber(QLCDNumber):
    def __init__(self, parent=None):
        QLCDNumber.__init__(self, parent)


