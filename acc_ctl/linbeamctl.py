import sys

if "pycx4.qcda" in sys.modules:
    import pycx4.qcda as cda
elif "pycx4.pycda" in sys.modules:
    import pycx4.pycda as cda


def linbeam_state(cav_h_val):
    if cav_h_val > 0:
        return 'open'
    if cav_h_val < -3000:
        return 'closed'
    return None


# the class to close linac beam with cav_h corrector and observe state
class LinBeamCtl:
    def __init__(self):
        super(LinBeamCtl, self).__init__()
        self.stateRequested = cda.InstSignal(str)
        self.stateChanged = cda.InstSignal(str)
        self.stateMeas = cda.InstSignal(str)

        self.cav_h_iset_chan = cda.DChan('canhw:11.rst1.CAV_H.Iset', on_update=True)
        self.cav_h_imeas_chan = cda.DChan('canhw:11.rst1.CAV_H.Imes', on_update=True)

        self.cav_h_iset_chan.valueChanged.connect(self.iset_cb)
        self.cav_h_imeas_chan.valueChanged.connect(self.imeas_cb)

        self.iset_saved = None
        self.state = None
        self.state_meas = None

    def iset_cb(self, chan):
        state = linbeam_state(chan.val)
        if state != self.state:
            self.state = state
            self.stateChanged.emit(state)

    def imeas_cb(self, chan):
        state_meas = linbeam_state(chan.val)
        if state_meas != self.state_meas:
            self.state_meas = state_meas
            self.stateMeas.emit(state_meas)

    def close_beam(self):
        if self.state == 'open':
            self.iset_saved = self.cav_h_iset_chan.val
            self.cav_h_iset_chan.setValue(-1.0 * self.iset_saved)

    def open_beam(self):
        if self.state == 'closed':
            if self.iset_saved is None:
                self.iset_saved = -1.0 * self.cav_h_iset_chan.val
            self.cav_h_iset_chan.setValue(self.iset_saved)

