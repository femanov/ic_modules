#
# machine modes server and client classes implementation
# by Fedor Emanov

from aux.Qt import QtCore
import pycx4.qcda as cda
import json
from settings.cx import *


def cmd_text(cmd, params={}):
    cdict = {}
    cdict['cmd'] = cmd
    cdict.update(params)
    return json.dumps(cdict)


# abstract mode ctl - base for others
class ModesCtl(QtCore.QObject):
    def __init__(self):
        super(ModesCtl, self).__init__()

        # create command and result channels
        self.cmd_chan = cda.StrChan(ctl_server + ".modectl.cmd@u")
        self.res_chan = cda.StrChan(ctl_server + ".modectl.res@u")
        self.cmd_chan.valueChanged.connect(self.cmd_cb)
        self.res_chan.valueMeasured.connect(self.res_cb)

    def cmd_cb(self, chan):
        pass

    def res_cb(self, chan):
        pass


class ModesClient(ModesCtl):
    # signals for mode save/load
    modeSaved = QtCore.pyqtSignal(dict)   # emited when recieved deamon mesage "mode saved"
    modeLoaded = QtCore.pyqtSignal(dict)  # emited when recieved deamon mesage "mode"

    # signals for automatic control
    markedLoad = QtCore.pyqtSignal(int)  # emited when switching to marked mode
    markedLoaded = QtCore.pyqtSignal(str)   # emited when switched to marked mode
    markedReady = QtCore.pyqtSignal()
    walkerDone = QtCore.pyqtSignal(str)

    #auxilary signals
    update = QtCore.pyqtSignal()  # emited when server instructs clients to update DB info

    def __init__(self, use_modeswitcher=False):
        super(ModesClient, self).__init__()

        # e_inj = 1, e_ext = 2, p_inj = 3, p_ext = 4
        self.mode = None
        self.timer = QtCore.QTimer()
        self.delay = 100

    def res_cb(self, chan):
        try:
            cdict = json.loads(chan.val)
        except:
            return
        if cdict['cmd'] == 'mode loaded':
            self.mode = None
            cdict['time'] = chan.time
            self.modeLoaded.emit(cdict)

        if cdict['cmd'] == 'mode saved':
            cdict['time'] = chan.time
            self.modeSaved.emit(cdict)

        if cdict['cmd'] == 'update':
            self.update.emit()

        if cdict['cmd'] == 'marked loaded':
            self.mode = cdict['mark_id']
            self.markedLoaded.emit(cdict['msg'])
            self.timer.singleShot(self.delay, self.emitMarkedReady)
            # 2do: not fully correct in case of user request during this wait. can be a race conditions

        if cdict['cmd'] == 'walker done':
            self.walkerDone.emit(cdict['name'])

    def setDelay(self, delay):
        self.delay = delay

    def emitMarkedReady(self):
        self.markedReady.emit()

    def save_mode(self, author, comment):
        self.cmd_chan.setValue(cmd_text('save', {'author':  author, 'comment': comment}))

    def load_mode(self, id, syslist, types):
        self.cmd_chan.setValue(cmd_text('load', {'id': id,
                                                 'syslist': syslist,
                                                 'types': types}))


    def load_marked(self, mark_id, syslist, types):
        self.cmd_chan.setValue(cmd_text('load marked', {'mark_id': mark_id,
                                                        'syslist': syslist,
                                                        'types': types}))

    def mark_mode(self, mode_id, name, comment, author, mark_id):
        self.cmd_chan.setValue(cmd_text('mark mode', {'mode_id': mode_id,
                                                      'name': name,
                                                      'comment': comment,
                                                      'author': author,
                                                      'mark_id': mark_id}))

    def walker_load(self, walkers_path):
        self.cmd_chan.setValue(cmd_text('walker load', {'walkers_path': walkers_path}))



class ModesServer(ModesCtl):
    save = QtCore.pyqtSignal(str, str)
    load = QtCore.pyqtSignal(int, list, list)
    loadMarked = QtCore.pyqtSignal(int, list, list)
    markMode = QtCore.pyqtSignal(int, str, str, str, int)
    walkerLoad = QtCore.pyqtSignal(dict)

    def __init__(self):
        super(ModesServer, self).__init__()

    def cmd_cb(self, chan):
        try:
            cdict = json.loads(chan.val)
        except:
            return
        if cdict['cmd'] == 'hello':
            self.res_chan.setValue(cmd_text('hello', {'msg': 'is online'}))

        if cdict['cmd'] == 'load':
            self.load.emit(cdict['id'], cdict['syslist'], cdict['types'])

        if cdict['cmd'] == 'save':
            self.save.emit(cdict['author'], cdict['comment'])

        if cdict['cmd'] == 'load marked':
            self.loadMarked.emit(cdict['mark_id'], cdict['syslist'], cdict['types'])

        if cdict['cmd'] == 'mark mode':
            self.markMode.emit(cdict['mode_id'], cdict['name'], cdict['comment'], cdict['author'], cdict['mark_id'])

        if cdict['cmd'] == 'walker load':
            self.walkerLoad.emit(cdict['walkers_path'])

        chan.setValue('')

    def saved(self, mode_id):
        self.res_chan.setValue(cmd_text('mode saved', {'mode_id': mode_id}))

    def loaded(self, msg):
        self.res_chan.setValue(cmd_text('mode loaded', {'msg': msg}))

    def update(self):
        self.res_chan.setValue(cmd_text('update', {}))

    def markedLoaded(self, mark_id, msg):
        self.res_chan.setValue(cmd_text('marked loaded', {'mark_id': mark_id, 'msg': msg}))

    def walkerDone(self, name):
        self.res_chan.setValue(cmd_text('walker done', {'name': name}))
