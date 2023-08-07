# iset-walker (Bolkhov's cx driver) interface-class
# walker interface channels:
# walker.list - requested list of points to go through
# walker.start - run process
# walker.stop - stop running
# walker.cur_step - current step, -1 when stopped (or finished)
# array example to demag spectrometer: a = [2500 * ((-0.7)**x) for x in range(20)]

from transitions import Machine
import numpy as np
import sys
if "pycx4.qcda" in sys.modules:
    import pycx4.qcda as cda
elif "pycx4.pycda" in sys.modules:
    import pycx4.pycda as cda


class MagWalker:
    def __init__(self, devname, name=None):
        self.stateNotify = cda.InstSignal(str)
        self.done = cda.InstSignal(str)
        self.progressing = cda.InstSignal(str, int)
        self.started = cda.InstSignal(str)
        self.intercepted = cda.InstSignal(str)

        self.devname = devname
        self.name = devname if name is None else name

        self.list_chan = cda.VChan(f'{devname}.walker.list', dtype=cda.DTYPE_DOUBLE, max_nelems=20, on_update=True)
        self.start_chan = cda.IChan(f'{devname}.walker.start', on_update=True)
        self.stop_chan = cda.IChan(f'{devname}.walker.stop', on_update=True)
        self.cur_step_chan = cda.IChan(f'{devname}.walker.cur_step', on_update=True)
        self.iset_cur_chan = cda.DChan(f'{devname}.iset_cur', on_update=True)
        self.iset_chan = cda.DChan(f'{devname}.iset', on_update=True)
        self.imeas_chan = cda.DChan(f'{devname}.imes', on_update=True)

        self.cur_list = None
        self.walk_requested = False
        self.progress = 0
        self.step = -2
        # self.step_pos = 0
        self.full_path = 0

        self.list_chan.valueMeasured.connect(self.list_update)
        self.cur_step_chan.valueChanged.connect(self.cur_step_update)
        self.iset_cur_chan.valueChanged.connect(self.iset_cur_update)
        self.iset_chan.valueChanged.connect(self.iset_update)

        self.states = ['unknown',
                  'failure',
                  {'name': 'stopped', 'on_enter': ['walk_stopped']},
                  'prepare',
                  {'name': 'walking', 'on_enter': ['walk_started']},
                  ]

        self.transitions = [
            {'trigger': 'init', 'source': 'unknown', 'dest': 'stopped', 'unless': ['is_walking']},
            {'trigger': 'init', 'source': 'unknown', 'dest': 'walking', 'conditions': ['is_walking']},
            {'trigger': 'update', 'source': ['walking', 'prepare'], 'dest': 'stopped', 'unless': ['is_walking']},
            {'trigger': 'update', 'source': ['stopped', 'prepare'], 'dest': 'walking', 'conditions': ['is_walking']},

            {'trigger': 'list_wait', 'source': 'stopped', 'dest': 'prepare'},

        ]

        self.m = Machine(model=self, states=self.states, transitions=self.transitions, initial='unknown',
                         after_state_change=self.state_notify)

    def state_notify(self):
        self.stateNotify.emit(self.state)

    def is_walking(self):
        return True if self.step >= 0 else False

    def walk_stopped(self):
        self.progress = 0
        self.done.emit(self.name)

    def walk_started(self):
        self.full_path = self.path_length(0)
        self.started.emit(self.name)

    def cur_step_update(self, chan):
        self.step = chan.val
        if self.state == 'unknown':
            self.init()
        if self.state in {'walking', 'prepare', 'stopped'}:
            self.update()

    def set_list(self, np_list):
        if self.state != 'stopped':
            # ignore setting list in not stopped state
            return
        self.list_chan.setValue(np_list)
        self.list_wait()

    def list_update(self, chan):
        self.cur_list = chan.val
        if self.walk_requested:
            self.start()

    def iset_cur_update(self, chan):
        if not self.state == 'walking':
            return
        pos = self.path_length(self.step)
        new_progress = int(100.0 * (1.0 - pos / self.full_path))
        if self.progress != new_progress:
            self.progress = new_progress
            self.progressing.emit(self.name, self.progress)

    def iset_update(self, chan):
        if self.state == 'walking':
            if np.abs(self.cur_list[self.step] - chan.val) < 2 * chan.quant:
                # here we think operator intercepted acc control
                print('control intercepted')

    def start(self):
        self.start_chan.setValue(1)
        self.walk_requested = True

    def stop(self):
        self.stop_chan.setValue(1)

    def run_list(self, np_list):
        self.set_list(np_list)
        self.walk_requested = True

    def path_length(self, step):
        start_iset = self.iset_cur_chan.val
        p_length = np.abs(self.cur_list[step] - start_iset)
        for ind in range(step, len(self.cur_list)-1):
            p_length += np.abs(self.cur_list[ind] - self.cur_list[ind+1])
        return p_length
