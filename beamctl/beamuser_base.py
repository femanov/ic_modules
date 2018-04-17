from PyQt5.QtCore import QObject
import pycx4.q5cda as cda


class BeamUserBase(QObject):
    def __init__(self, name, ctl_dev):
        super(BeamUserBase, self).__init__()
        self.name = name

        # create command and result channels
        # @u means that is's unbuffered
        self.req_chan = cda.StrChan(ctl_dev + ".request@u")
        self.ans_chan = cda.StrChan(ctl_dev + ".answer@u")
        self.req_chan.valueMeasured.connect(self.req_cb)
        self.ans_chan.valueMeasured.connect(self.ans_cb)

    def req_cb(self, chan):
        print('new request', chan.val)

    def ans_cb(self, chan):
        print('new answer', chan.val)
