from pycx4.cda import InstSignal, IChan, Timer
from transitions import Machine

clock_names = {
    "off":    0,
    "vepp2k": 1,
    "vepp3":  2,
    "test":   3,
}

states = ['fail',               # if some command not finished in expected time
          'unknown',            # just started, no operation data yet
          'ready',              # ready for trigger
          'triggered',          # triggered
          'prepare',            # shot requested
          'continuous'          # operating in continuous mode <-- very rear
          ]

transitions = [
    # initial transitions
    {'trigger': 'init', 'source': 'unknown', 'dest': 'continuous', 'unless': ['is_single_mode']},
    {'trigger': 'init', 'source': 'unknown', 'dest': 'ready', 'conditions': ['is_single_mode'],
     'unless': ['was_triggered']},
    {'trigger': 'init', 'source': 'unknown', 'dest': 'triggered', 'conditions': ['is_single_mode', 'was_triggered']},

    # when recieved data about runmode
    {'trigger': 'mode_update', 'source': 'continuous', 'dest': 'ready', 'conditions': ['is_single_mode'],
     'unless': ['was_triggered']},
    {'trigger': 'mode_update', 'source': 'continuous', 'dest': 'triggered',
     'conditions': ['is_single_mode', 'was_triggered']},
    {'trigger': 'mode_update', 'source': ['ready', 'triggered'], 'dest': 'continuous', 'unless': ['is_single_mode']},

    {'trigger': 'trigger_reset', 'source': 'triggered', 'dest': 'ready'},
    {'trigger': 'do_shot', 'source': 'triggered', 'dest': 'prepare'},
    {'trigger': 'ready_confirmed', 'source': 'prepare', 'dest': 'ready'},
    {'trigger': 'shot_done', 'source': ['ready', 'prepare'], 'dest': 'triggered'},

    # {'trigger': '', 'source': '', 'dest': ''},
]


class Extractor:
    def __init__(self):
        super().__init__()
        self.extractionDone = InstSignal()
        self.unexpectedShot = InstSignal()
        self.trainingShot = InstSignal()
        self.trainingStopped = InstSignal()

        self.m = Machine(model=self, states=states, transitions=transitions, initial='unknown',
                         after_state_change=self.state_notify)

        self.mode = None
        self.trigger_fired = None

        # self.c_clock_src = IChan("canhw:19.ic.extractor.clockSrc", on_update=True)
        # self.c_clock_src.valueChanged.connect(self.clock_src_update)
        self.c_do_shot = IChan("canhw:19.xfr_d16_20.do_shot",  on_update=True)
        self.c_stop = IChan("canhw:19.xfr_d16_20.ones_stop",  on_update=True)
        self.c_mode = IChan('canhw:19.xfr_d16_20.mode', on_update=True)
        self.c_was_shot = IChan("canhw:19.xfr_d16_20.was_start",  on_update=True)

        self.c_mode.valueChanged.connect(self.c_mode_cb)
        self.c_was_shot.valueMeasured.connect(self.c_was_shot_cb)

        self.timer = Timer()

    def state_notify(self):
        print(self.state)

    def is_single_mode(self):
        return True if self.mode == 'single' else False

    def was_triggered(self):
        return self.trigger_fired

    def c_mode_cb(self, chan):
        self.mode = 'single' if chan.val == 1 else 'continuous'
        if self.state == 'unknown':
            if self.trigger_fired is not None:
                self.init()
            return
        else:
            self.mode_update()

    def c_was_shot_cb(self, chan):
        self.trigger_fired = bool(chan.val)
        if self.state == 'unknown':
            if self.mode is not None:
                self.init()
            return
        if chan.val == 0:
            if self.state == 'prepare':
                self.ready_confirmed()
                return
            elif self.state == 'triggered':
                self.trigger_reset()
                # this usually means someone else requested shot
                return
            else:
                print('was_shot processing.. wrong state: ', self.state)
        if chan.val == 1:
            if self.state in ['ready', 'prepare']:
                self.shot_done()
                self.extractionDone.emit()
                return
            else:
                print('was_shot processing.. wrong state: ', self.state)

    def extract(self):
        if self.state == 'triggered':
            self.c_do_shot.setValue(1)
            self.do_shot()
        else:
            print('wrong state')

    def stop(self):
        if self.state in ['ready', 'prepare']:
            self.c_stop.setValue(1)

    def set_mode(self, mode_name):
        if mode_name == 'single':
            self.c_mode.setValue(1)
        elif mode_name == 'continuous':
            self.c_mode.setValue(0)
        else:
            print('wrong mode')
