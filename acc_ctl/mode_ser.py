# machine modes server and client classes implementation
# by Fedor Emanov
import sys
import json
if "pycx4.qcda" in sys.modules:
    import pycx4.qcda as cda
elif "pycx4.pycda" in sys.modules:
    import pycx4.pycda as cda

from settings.cx import ctl_server

def cmd_text(cmd, params={}):
    cdict = {}
    cdict['cmd'] = cmd
    cdict.update(params)
    return json.dumps(cdict)


# abstract mode ctl - base for others
class ModesCtl:
    def __init__(self):
        super().__init__()

        # create command and result channels
        self.cmd_chan = cda.StrChan(ctl_server + ".modectl.cmd", max_nelems=1024, on_update=True, privete=True)
        self.res_chan = cda.StrChan(ctl_server + ".modectl.res", max_nelems=1024, on_update=True, privete=True)
        self.cmd_chan.valueChanged.connect(self.cmd_cb)
        self.res_chan.valueMeasured.connect(self.res_cb)

    def cmd_cb(self, chan):
        pass

    def res_cb(self, chan):
        pass


class ModesClient(ModesCtl):
    # signals for mode save/load
    modeSaved = cda.Signal(dict)   # emited when recieved deamon mesage "mode saved"
    modeLoaded = cda.Signal(dict)  # emited when recieved deamon mesage "mode"
    zerosDone = cda.Signal(dict)
    # signals for automatic control
    markedLoaded = cda.Signal(str)   # emited when switched to marked mode
    markedReady = cda.Signal()
    walkerDone = cda.Signal(str)
    #auxilary signals
    update = cda.Signal()  # emited when server instructs clients to update DB info

    def __init__(self, use_modeswitcher=False):
        super(ModesClient, self).__init__()

        self.mode_mark = None
        self.timer = cda.Timer()
        self.delay = 100

        self.proto_ver = 0.901

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
            self.mode_mark = cdict['mark']
            self.markedLoaded.emit(cdict['msg'])
            self.timer.singleShot(self.delay, self.emitMarkedReady)
            # 2do: not fully correct in case of user request during this wait. can be a race conditions

        if cdict['cmd'] == 'walker done':
            self.walkerDone.emit(cdict['name'])

        if cdict['cmd'] == 'zeros done':
            cdict['time'] = chan.time
            self.modeLoaded.emit(cdict)


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

    def load_marked(self, mark, syslist, types=['rw']):
        self.cmd_chan.setValue(cmd_text('load marked', {'mark': mark,
                                                        'syslist': syslist,
                                                        'types': types}))

    def set_zeros(self, syslist, types=['rw']):
        self.cmd_chan.setValue(cmd_text('set zeros', {'syslist': syslist,
                                                      'types': types}))

    def mark_mode(self, mode_id, mark, comment, author):
        self.cmd_chan.setValue(cmd_text('mark mode', {'mode_id': mode_id,
                                                      'mark': mark,
                                                      'comment': comment,
                                                      'author': author}))

    def walker_load(self, walkers_path, coefs):
        self.cmd_chan.setValue(cmd_text('walker load', {'walkers_path': walkers_path,
                                                        'coefs': coefs}))

    def ask_update(self):
        self.res_chan.setValue(cmd_text('update', {}))


class ModesServer(ModesCtl):
    save = cda.Signal(str, str)
    load = cda.Signal(int, list, list)
    loadMarked = cda.Signal(str, list, list)
    setZeros = cda.Signal(list, list)
    markMode = cda.Signal(int, str, str, str)
    walkerLoad = cda.Signal(dict, dict)

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
            self.loadMarked.emit(cdict['mark'], cdict['syslist'], cdict['types'])

        if cdict['cmd'] == 'mark mode':
            self.markMode.emit(cdict['mode_id'], cdict['mark'], cdict['comment'], cdict['author'])

        if cdict['cmd'] == 'walker load':
            self.walkerLoad.emit(cdict['walkers_path'], cdict['coefs'])

        if cdict['cmd'] == 'set zeros':
            self.setZeros.emit(cdict['syslist'], cdict['types'])

        chan.setValue('')

    def saved(self, mode_id):
        self.res_chan.setValue(cmd_text('mode saved', {'mode_id': mode_id}))

    def loaded(self, msg):
        self.res_chan.setValue(cmd_text('mode loaded', {'msg': msg}))

    def update(self):
        self.res_chan.setValue(cmd_text('update', {}))

    def markedLoaded(self, mark, msg):
        self.res_chan.setValue(cmd_text('marked loaded', {'mark': mark, 'msg': msg}))

    def walkerDone(self, name):
        self.res_chan.setValue(cmd_text('walker done', {'name': name}))

    def zerosDone(self, msg):
        self.res_chan.setValue(cmd_text('zeros done', {'msg': msg}))
