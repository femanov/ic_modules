from pycx4.pycda import InstSignal, IChan, StrChan, Timer
from transitions import Machine

states = ['fail',               # if some command not finished in expected time
          'unknown',            # just started, no operation data yet
          'switching_runmode',  # we ordered to switch runmode
          'continuous',         # operating in continuous mode
          'counter_idle',       # counter mode idle
          'counter_start',      # counter mode start command issues
          'counter_run']        # counter running

transitions = [
    # initial transitions
    {'trigger': 'init', 'source': 'unknown', 'dest': 'continuous', 'unless': ['is_counter']},
    {'trigger': 'init', 'source': 'unknown', 'dest': 'counter_idle', 'conditions': ['is_counter'],
     'unless': ['is_running']},
    {'trigger': 'init', 'source': 'unknown', 'dest': 'counter_run', 'conditions': ['is_counter', 'is_running']},

    # when runmode switching requested
    {'trigger': 'switch_runmode', 'source': ['continuous', 'counter_idle', 'counter_run'], 'dest': 'switching_runmode'},

    # when recieved data about runmode
    {'trigger': 'runmode_update', 'source': ['continuous', 'switching_runmode'], 'dest': 'counter_idle',
     'conditions': ['is_counter']},
    {'trigger': 'runmode_update', 'source': ['counter_run', 'counter_idle', 'switching_runmode'], 'dest': 'continuous',
     'unless': ['is_counter']},

    {'trigger': 'run_request', 'source': 'counter_idle', 'dest': 'counter_start'},
    {'trigger': 'running_update', 'source': ['counter_idle', 'counter_start'], 'dest': 'counter_run', 'conditions': ['is_running']},
    {'trigger': 'run_done', 'source': 'counter_run', 'dest': 'counter_idle'},
    {'trigger': 'run_timed_out', 'source': 'counter_run', 'dest': 'fail'},
    {'trigger': 'reset', 'source': 'fail', 'dest': 'unknown'},

    # {'trigger': 'update', 'source': 'counter_idle', 'dest': 'counter_run',
    #  'conditions': ['is_counter', 'is_running']},

    # {'trigger': 'update', 'source': '*', 'dest': 'on', 'conditions': ['is_on']},
    # {'trigger': 'update', 'source': '*', 'dest': 'off', 'conditions': ['is_off']},
    # {'trigger': 'update', 'source': '*', 'dest': 'turning_on', 'conditions': ['is_turning_on']},
    # {'trigger': 'update', 'source': '*', 'dest': 'turning_off', 'conditions': ['is_turning_off']},
    # {'trigger': '', 'source': '', 'dest': ''},
    # {'trigger': '', 'source': '', 'dest': ''},

    # 2DO: timeout on transition to failed state
]


class LinStarter:
    def __init__(self):
        super().__init__()
        self.runmodeChanged = InstSignal(str)
        self.nshotsChanged = InstSignal(int)
        self.runDone = InstSignal()

        self.m = Machine(model=self, states=states, transitions=transitions, initial='unknown',
                         after_state_change=self.state_notify)

        # state variables.
        self.runmode = None
        self.runmode_req = False
        self.running = False
        self.run_req = False
        self.nshots = 0  # number of requested shots
        self.nshots_req = False

        self.c_runmode = IChan('syn_ie4.mode', on_update=True)
        self.c_running = IChan('syn_ie4.bum_going', on_update=True)
        self.c_lamsig = IChan('syn_ie4.lam_sig', on_update=True)
        self.c_start = IChan('syn_ie4.bum_start', on_update=True)
        self.c_stop = IChan('syn_ie4.bum_stop', on_update=True)
        self.c_nshots = IChan('syn_ie4.re_bum', on_update=True)

        self.c_runmode.valueChanged.connect(self.c_runmode_cb)
        self.c_running.valueChanged.connect(self.c_running_cb)
        self.c_nshots.valueChanged.connect(self.nshots_update)
        self.c_lamsig.valueMeasured.connect(self.c_lamsig_cb)

        self.c_state = StrChan('linstarter.state', max_nelems=30)
        self.c_runmode_t = StrChan('linstarter.runmode', max_nelems=20)

        self.run_timeout = Timer()

    def state_notify(self):
        print(self.state)
        self.c_state.setValue(self.state)

    def c_runmode_cb(self, chan):
        self.runmode = 'counter' if chan.val == 1 else 'continuous'  # not totally correct
        if self.state == 'unknown':
            self.init()
        elif self.state in ['counter_run', 'continuous', 'counter_idle', 'switching_runmode']:
            self.runmode_update()
        self.c_runmode_t.setValue(self.runmode)
        self.runmodeChanged.emit(self.runmode)

    def c_running_cb(self, chan):
        self.running = bool(chan.val)
        print('running:', self.running)
        if self.state == 'counter_idle' or self.state == 'counter_start':
            self.running_update()

    def c_lamsig_cb(self, chan):
        print('LAM recieved')
        self.running = False
        self.run_done()

    def is_counter(self):
        return True if self.runmode == 'counter' else False

    def is_running(self):
        return self.running

    def set_runmode(self, runmode):
        if self.runmode != runmode:
            self.c_runmode.setValue(1 if self.runmode == 'counter' else 0)
            self.runmode_req = True

    def nshots_update(self, chan):
        self.nshots = chan.val
        self.nshots_req = False
        self.nshotsChanged.emit(self.nshots)

    def set_nshots(self, nshots):
        if self.state == 'counter_idle':
            if self.nshots != nshots:
                self.c_nshots.setValue(nshots)
                self.nshots_req = True
        else:
            print('wrong state to set nshots')

    def start(self):
        if self.state == 'counter_idle':
            self.c_start.setValue(1)
            self.run_request()
        else:
            print('wrong state to start')

    def stop(self):
        if self.state == 'counter_run':
            self.c_stop.setValue(1)
        else:
            print('wrong state to stop')

    def shots_left_update(self, chan):
        pass


