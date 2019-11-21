#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication
from fwidgets import CXSwitch

app = QApplication(sys.argv)
#w = CXLCDNumber(None, 'canhw:13.BUN1.Imes')
#w.show()

#w2 = CXCheckBox(cname='Ql1.Iset')
#w2.show()

w3 = CXSwitch(cname='cxhw:0.ddm.v2k_auto')
w3.show()
dir(CXSwitch)

sys.exit(app.exec_())
