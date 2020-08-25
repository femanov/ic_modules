import sys
import numpy as np
import time

if "pycx4.qcda" in sys.modules:
    import pycx4.qcda as cda
elif "pycx4.pycda" in sys.modules:
    import pycx4.pycda as cda

from acc_ctl.magwalker import MagWalker
from acc_ctl import mode_ser
from acc_ctl.mode_defs import *

remag_srv = 'canhw:12'
remag_devs = ['d3m4n5', 'd5M1t4', 'd6M1t4']


# hardcoded values for some energy
remag_vals = {
    'e2v2': {'d3m4n5': 262.0, 'd5M1t4': -831.0, 'd6M1t4': -831.0},
    'p2v2': {'d3m4n5': 0.0, 'd5M1t4': 839.0, 'd6M1t4': 838.0},
    'e2v4': {'d3m4n5': 262.0, 'd5M1t4': -831.0, 'd6M1t4': 0.0},
    'p2v4': {'d3m4n5': 0.0, 'd5M1t4': 839.0, 'd6M1t4': 0.0}
}

remag_tolerance = 0.05

def remag_mode(val_dict):
    for mode in remag_vals:
        this_mode = True
        for mag in remag_vals[mode]:
            v1 = remag_vals[mode][mag]
            v2 = val_dict[mag]
            if np.abs(v1 - v2) > np.abs(v1) * remag_tolerance and np.abs(v1 - v2) > 5:
                this_mode = False
                break
        if this_mode:
            return mode
    return None


class K500Director:
    done = cda.Signal()
    modeTargUpdate = cda.Signal(str)
    modeCurUpdate = cda.Signal(str)
    progressing = cda.Signal(int)

    def __init__(self):
        super(K500Director, self).__init__()

        self.mode_ctl = mode_ser.ModesClient()

        self.walkers = {name: MagWalker(remag_srv + '.' + name, name) for name in remag_devs}

        for k in self.walkers:
            w = self.walkers[k]
            w.done.connect(self.check_done)
            w.started.connect(self.check_started)
            w.progressing.connect(self.all_progress)
            w.iset_chan.valueMeasured.connect(self.target_mode)
            w.imeas_chan.valueMeasured.connect(self.current_mode)

        self.running = False
        self.cur_mode = None
        self.mode_targ = None
        self.progress = 0

        self.swc_time = 0
        self.start_time = 0

    def check_done(self, name):
        for k in self.walkers:
            if self.walkers[k].running:
                return
        self.swc_time = time.time() - self.start_time
        self.running = False
        self.progress = 0
        self.progressing.emit(100)
        self.done.emit()

    def check_started(self, name):
        self.running = True
        self.start_time = time.time()

    def target_mode(self, chan):
        if self.running:
            vals = {n: self.walkers[n].cur_list[-1] for n in self.walkers}
        else:
            vals = {n: self.walkers[n].iset_chan.val for n in self.walkers}
        mode = remag_mode(vals)
        if self.mode_targ != mode:
            self.mode_targ = mode
            self.modeTargUpdate.emit(self.mode_targ)

    def current_mode(self, chan):
        vals = {n: self.walkers[n].imeas_chan.val for n in self.walkers}
        mode = remag_mode(vals)
        if self.cur_mode != mode:
            self.cur_mode = mode
            self.modeCurUpdate.emit(self.cur_mode)

    def all_progress(self, name, progress):
        if self.running:
            all_prg = progress
            for k in self.walkers:
                w = self.walkers[k]
                if w.progress < all_prg and w.running:
                    all_prg = w.progress
            self.progress = all_prg
            self.progressing.emit(all_prg)

    def set_mode(self, target_mode):
        if target_mode == self.cur_mode:
            return
        mag_path = {name: mode_path(name, self.cur_mode, target_mode) for name in remag_devs}
        coefs = {name: coefs_set[name][path_set[name].index(mag_path[name])] for name in mag_path}
        print(coefs)
        self.mode_ctl.walker_load(mag_path, coefs)

