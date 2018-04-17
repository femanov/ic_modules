from aux.Qt import QtCore
from pycx4.qcda import cda

#from PyQt5.QtCore import QObject, pyqtSignal

from settings.cx import ddm_dev

# options (chans which both client and server can update)
_option_names = ['ClockSrc', 'Eshots', 'Pshots', 'LinRunmode', 'ModeDelay', 'Particles']
# commands
_command_names = ['linrun', 'extract', 'nround', 'autorun', 'stop']
# events
_event_names = ['preparing2inject',
                'injecting',
                'injected',
                'preparing2extract',
                'extracting',
                'extracted']
# information
_info_names = ['nshots', 'state']


def register_chans2dict(namelist, callback=None):
    chans = {k: cda.DChan(ddm_dev + '.' + k + '@u') for k in namelist}
    if callback is not None:
        for c in chans.values():
            c.valueChanged.connect(callback)
    return chans

# ------------------------------


class DdmAbstract(QtCore.QObject):
    updateClockSrc = QtCore.pyqtSignal(float)
    updateEshots = QtCore.pyqtSignal(float)
    updatePshots = QtCore.pyqtSignal(float)
    updateLinRunmode = QtCore.pyqtSignal(float)
    updateModeDelay = QtCore.pyqtSignal(float)
    updateParticles = QtCore.pyqtSignal(float)

    def __init__(self):
        super(DdmAbstract, self).__init__()
        self.option_chans = register_chans2dict(_option_names, self.update_option)

    def update_option(self, chan):
        print("update", chan.short_name())
        getattr(self, "update" + chan.short_name()).emit(chan.val)

# ------------------------------


class DdmServer(DdmAbstract):
    linrunRecieved = QtCore.pyqtSignal()
    extractRecieved = QtCore.pyqtSignal()
    nroundRecieved = QtCore.pyqtSignal(int)
    autorunRecieved = QtCore.pyqtSignal()
    stopRecieved = QtCore.pyqtSignal()

    def __init__(self):
        super(DdmServer, self).__init__()
        self.cmd_chans = register_chans2dict(_command_names, self.cmd_proc)
        self.event_chans = register_chans2dict(_event_names)
        self.info_chans = register_chans2dict(_info_names)
        self.msgchan = cda.StrChan(ddm_dev + '.' + 'stateMag' + '@u')

    def cmd_proc(self, chan):
        if int(chan.val) > 0:
            name = chan.short_name()
            if name == 'linrun':
                self.linrunRecieved.emit()
            if name == 'extract':
                self.extractRecieved.emit()
            if name == 'nround':
                self.nroundRecieved.emit(int(chan.val))
            if name == 'autorun':
                self.autorunRecieved.emit()
            if name == 'stop':
                self.stopRecieved.emit()
            chan.setValue(0)
            print(name)

    # may be rewrite to autogenerate event senders
    def event_send(self, name):
        c = self.event_chans[name]
        c.setValue(c.val + 1)

    def preparing2inject_send(self):
        self.event_send('preparing2inject')

    def injecting_send(self):
        self.event_send('injecting')

    def injected_send(self):
        self.event_emit('injected')

    def preparing2extract_send(self):
        self.event_send('preparing2inject')

    def extracting(self):
        self.event_send('extracting')

    def extracted_send(self):
        self.event_send('extracted')

# ------------------------------


class DdmClient(DdmAbstract):
    nshotsUpdate = QtCore.pyqtSignal(float)
    stateUpdate = QtCore.pyqtSignal(float)

    preparing2inject = QtCore.pyqtSignal()
    injecting = QtCore.pyqtSignal()
    injected = QtCore.pyqtSignal()
    preparing2extract = QtCore.pyqtSignal()
    extracting = QtCore.pyqtSignal()
    extracted = QtCore.pyqtSignal()

    def __init__(self):
        super(DdmClient, self).__init__()
        self.cmd_chans = register_chans2dict(_command_names)
        self.event_chans = register_chans2dict(_event_names, self.event_reciev)
        self.info_chans = register_chans2dict(_info_names, self.info_update)
        self.msgchan = cda.StrChan(ddm_dev + '.' + 'stateMag' + '@u')

    def event_reciev(self, chan):
        getattr(self, chan.short_name()).emit()

    def run_command(self, name, val=1):
        self.cchans[name].setValue(val)

    # may be better to autogenerate command methond
    def linrun(self):
        self.run_command('linrun')

    def extract(self):
        self.run_command('extract')

    def round(self):
        self.run_command('nround')

    def autorun(self):
        self.run_command('autorun')

    def stop(self):
        self.run_command('stop')

    def nround(self, n):
        self.run_command('nround', n)

    def info_update(self, chan):
        if chan.short_name() == 'nshots':
            self.nshotsUpdate.emit(chan.val)
        if chan.short_name() == 'state':
            self.stateUpdate.emit(chan.val)

