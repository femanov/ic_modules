import sys
import json
if "pycx4.qcda" in sys.modules:
    import pycx4.qcda as cda
elif "pycx4.pycda" in sys.modules:
    import pycx4.pycda as cda


class DaemonCtl:
    def __init__(self, ctrl_dev, srv=True):
        super().__init__()
        # create command and result channels
        self.cmd_chan = cda.StrChan(f'{ctrl_dev}.cmd', max_nelems=1024, on_update=True, privete=True)
        self.res_chan = cda.StrChan(f'{ctrl_dev}.res', max_nelems=1024, on_update=True, privete=True)
        self.cmd_chan.valueChanged.connect(self.cmd_cb)
        self.res_chan.valueMeasured.connect(self.res_cb)
        self.srv = srv

        # creating signa
        print(self.commands)
        for x in self.commands:
            if hasattr(self, x):
                print('Warning! Attribute mapping intersection!')
            setattr(self, x, cda.InstSignal(object))

    def cmd_cb(self, chan):
        if self.srv:
            cdict = self.parse_pack(chan.val)
            chan.setValue('')
            if cdict is None:
                return
            if 'cmd' in cdict:
                if cdict['cmd'] == 'alive?':
                    self.send_pack('alive')
                if hasattr(self, cdict['cmd']):
                    getattr(self, cdict['cmd']).emit(cdict)

    def res_cb(self, chan):
        if not self.srv:
            cdict = self.parse_pack(chan.val)
            if cdict is None:
                return

    def parse_pack(self, pack_str):
        try:
            cdict = json.loads(pack_str)
            return cdict
        except:
            return None

    def send_pack(self, cmd, params={}):
        cdict = {'cmd': cmd}
        cdict.update(params)
        chan = self.res_chan if self.srv else self.cmd_chan
        chan.setValue(json.dumps(cdict))

