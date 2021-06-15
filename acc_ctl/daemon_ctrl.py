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
        self.cmd_chan = cda.StrChan(ctrl_dev + ".cmd", max_nelems=1024, on_update=True, privete=True)
        self.res_chan = cda.StrChan(ctrl_dev + ".res", max_nelems=1024, on_update=True, privete=True)
        self.cmd_chan.valueChanged.connect(self.cmd_cb)
        self.res_chan.valueMeasured.connect(self.res_cb)
        self.srv = srv

    def cmd_cb(self, chan):
        if self.srv:
            cdict = self.parse_pack(chan.val)
            chan.setValue('')
            if cdict is None:
                return
            self.reaction(cdict)

    def res_cb(self, chan):
        if not self.srv:
            cdict = self.parse_pack(chan.val)
            if cdict is None:
                return
            self.reaction(cdict)

    def reaction(self, cdict):
        print(cdict)

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

