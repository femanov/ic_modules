from aux.Qt import QtCore
import pycx4.qcda as cda
import numpy as np

# array example to demag spectrometer: a = [2500 * ((-0.7)**x) for x in range(20)]


class MagWalker(QtCore.QObject):
    done = QtCore.pyqtSignal(str)
    progressing = QtCore.pyqtSignal(str, int)
    started = QtCore.pyqtSignal(str)

    def __init__(self, devname, name=None):
        super(MagWalker, self).__init__()
        self.devname = devname
        self.name = name
        if name is None:
            self.name = devname

        # channels:
        # walker.list - requested list of points to go through
        # walker.start - run process
        # walker.stop - stop running
        # walker.cur_step - current step, -1 when stopped (or finished)
        self.list_chan = cda.VChan(devname + '.walker.list', dtype=cda.DTYPE_DOUBLE, max_nelems=20, on_update=True)
        self.start_chan = cda.DChan(devname + '.walker.start', on_update=True)
        self.stop_chan = cda.DChan(devname + '.walker.stop', on_update=True)
        self.cur_step_chan = cda.DChan(devname + '.walker.cur_step', on_update=True)
        self.iset_cur_chan = cda.DChan(devname + '.iset_cur', on_update=True)
        self.iset_chan = cda.DChan(devname + '.iset', on_update=True)

        # just for some control
        self.imeas_chan = cda.DChan(devname + '.imes', on_update=True)

        self.initialized = False
        self.cur_list = None
        self.requested_list = None
        self.run_requested = False
        self.running = False
        self.progress = 0
        self.step = -1
        self.step_pos = 0
        self.path_length = 0
        self.start_iset = 0
        self.ext_cur_list = None

        self.list_chan.valueMeasured.connect(self.list_update)
        self.cur_step_chan.valueChanged.connect(self.step_update)
        self.iset_cur_chan.valueChanged.connect(self.iset_cur_update)

    def iset_update(self, chan):
        if self.step >= 0:
            if np.abs(self.cur_list[self.step] - chan.val) < 2 * chan.quant:
                # here we think operator intercepted acc control
                self.stop()

    def list_update(self, chan):
        if not self.initialized:
            self.initialized = True
        self.cur_list = chan.val
        self.ext_cur_list = np.zeros(len(self.cur_list) + 1)
        self.ext_cur_list[1:] = self.cur_list
        if self.requested_list is not None:
            self.set_list(self.requested_list)
            self.requested_list = None
            return
        if self.run_requested:
            self.start()

    def step_update(self, chan):
        self.step = int(chan.val)
        if self.step == -1 and self.running:
            self.running = False
            self.progress = 0
            self.done.emit(self.name)
            return
        if self.step == 0:
            self.step_pos = 0
            self.running = True  # if somebody else run walker - we correct state flag.
            self.update_path_length()
            self.started.emit(self.name)
            # line above may be not fully correct

        if self.step > 0:
            self.step_pos += np.abs(self.ext_cur_list[self.step-1] - self.ext_cur_list[self.step])

    def iset_cur_update(self, chan):
        if not self.running:
            return
        pos = self.step_pos + np.abs(self.ext_cur_list[self.step] - chan.val)
        new_progress = int(100.0 * pos / self.path_length)
        if self.progress != new_progress:
            self.progress = new_progress
            self.progressing.emit(self.name, self.progress)

    def set_list(self, np_list):
        if self.initialized:
            self.list_chan.setValue(np_list)
        else:
            self.requested_list = np_list

    def start(self):
        self.update_path_length()
        self.start_chan.setValue(1)
        self.running = True
        self.started.emit(self.name)

    def stop(self):
        self.stop_chan.setValue(1)

    def run_list(self, np_list):
        self.set_list(np_list)
        self.run_requested = True

    def update_path_length(self):
        self.start_iset = self.iset_cur_chan.val
        self.ext_cur_list[0] = self.start_iset
        self.path_length = 0
        for ind in range(len(self.ext_cur_list)-1):
            self.path_length += np.abs(self.ext_cur_list[ind] - self.ext_cur_list[ind+1])
