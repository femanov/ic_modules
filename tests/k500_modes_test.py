#!/usr/bin/env python3

import signal
import pycx4.pycda as cda
from acc_ctl.k500modes import K500Director

signal.signal(signal.SIGINT, signal.SIG_DFL)


k500 = K500Director()
print(k500.cur_mode)
k500.modeCurUpdate.connect(print)


cda.main_loop()
