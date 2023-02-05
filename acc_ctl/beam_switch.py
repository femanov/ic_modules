import pycx4.pycda as cda
from transitions import Machine


class LinBeamSwitch:
    def __init__(self):
        self.states = ['unknown', 'on', 'off', 'turning_on', 'turning_off', 'failed']
        self.state_codes = {
            'failed': -2,
            'unknown': -1,
            'off': 0,
            'on': 1,
            'turning_off': 2,
            'turning_on': 3,
        }
        self.transitions = [
            {'trigger': 'update', 'source': '*', 'dest': 'unknown', 'conditions': ['is_unknown']},
            {'trigger': 'update', 'source': '*', 'dest': 'on', 'conditions': ['is_on']},
            {'trigger': 'update', 'source': '*', 'dest': 'off', 'conditions': ['is_off']},
            {'trigger': 'update', 'source': '*', 'dest': 'turning_on', 'conditions': ['is_turning_on']},
            {'trigger': 'update', 'source': '*', 'dest': 'turning_off', 'conditions': ['is_turning_off']},
            # {'trigger': '', 'source': '', 'dest': ''},
            # 2DO: timeout on transition to failed state
        ]

        self.m = Machine(model=self,
                         states=self.states,
                         transitions=self.transitions,
                         initial='unknown',
                         after_state_change=self.state_notify)

        self.cav_h_iset_chan = cda.DChan('rst1.CAV_H.Iset', on_update=True)
        self.cav_h_imeas_chan = cda.DChan('rst1.CAV_H.Imes', on_update=True)

        self.cav_h_imeas_chan.setTolerance(10.0)  # 10 mA to react
        self.i_set = 0
        self.i_meas = 0
        self.cav_h_iset_chan.valueChanged.connect(self.iset_update)
        self.cav_h_imeas_chan.valueChanged.connect(self.imeas_update)

        self.on_chan = cda.IChan('BeamSwitch.switch_on', on_update=True)
        self.on_chan.valueMeasured.connect(self.on_chan_reaction)
        self.off_chan = cda.IChan('BeamSwitch.switch_off', on_update=True)
        self.off_chan.valueMeasured.connect(self.off_chan_reaction)
        self.is_on_chan = cda.IChan('BeamSwitch.is_on')
        self.state_chan = cda.IChan('BeamSwitch.state')
        self.state_t_chan = cda.StrChan('beamswitch.state_t', max_nelems=100)

    def state_notify(self):
        self.state_chan.setValue(self.state_codes[self.state])
        self.state_t_chan.setValue(self.state)
        self.is_on_chan.setValue(1 if self.state == 'on' else 0)

    def is_unknown(self):
        return True if (self.i_meas < 4000 and self.i_meas > -4000) or (self.i_set < 4000 and self.i_set > -4000) else False

    def is_on(self):
        return True if self.i_meas > 4000 and self.i_set > 4000 else False

    def is_off(self):
        return True if self.i_meas < -4000 and self.i_set < -4000 else False

    def is_turning_on(self):
        return True if self.i_meas < 4000 and self.i_set > 4000 else False

    def is_turning_off(self):
        return True if self.i_meas > -4000 and self.i_set < -4000 else False

    def switch_on(self):
        self.cav_h_iset_chan.setValue(4500)

    def switch_off(self):
        self.cav_h_iset_chan.setValue(-4500)

    def iset_update(self, chan):
        self.i_set = self.cav_h_iset_chan.val
        self.update()

    def imeas_update(self, chan):
        self.i_meas = self.cav_h_imeas_chan.val
        self.update()

    def off_chan_reaction(self, chan):
        if chan.val == 1:
            chan.setValue(0)
            self.switch_off()

    def on_chan_reaction(self, chan):
        if chan.val == 1:
            chan.setValue(0)
            self.switch_on()

