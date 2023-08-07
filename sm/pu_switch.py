from pycx4.cda import InstSignal, DChan, Timer
from transitions import Machine
from ic_modules.acc_ctl.k500modes import k500_mode

remag_srv = 'canhw:12'
remag_devs = ['d3m4n5', 'd5M1t4', 'd6M1t4']

states = ['unknown', 'switching', 'e2v2', 'p2v2', 'e2v4', 'p2v4']

transitions = []


class PUSwitch:
    def __init__(self):
        self.stateNotify = InstSignal(str)



        self.m = Machine(model=self, states=states, transitions=transitions, initial='unknown',
                         after_state_change=self.state_notify)

