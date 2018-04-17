# message sending class to request beam from injection complex
# by Fedor Emanov

from PyQt5.QtCore import pyqtSignal
import json
from aux import cmd_text
from beamctl.beamuser_base import BeamUserBase


class BeamUserCly(BeamUserBase):
    beamDenied = pyqtSignal(str)
    requestAccepted = pyqtSignal()
    confirmedReject = pyqtSignal()
    confirmedPause = pyqtSignal()

    def __init__(self, name, ctl_dev):
        super(BeamUserCly, self).__init__(name, ctl_dev)

    def req_cb(self, chan):
        pass

    def ans_cb(self, chan):
        try:
            cdict = json.loads(chan.val)
        except:
            return
        if cdict['cmd'] == 'beam denied':
            self.beamDenied.emit(cdict['reason'])
        if cdict['cmd'] == 'request accepted':
            self.requestAccepted.emit()
        if cdict['cmd'] == 'reject confirmed':
            self.confirmedReject.emit()
        if cdict['cmd'] == 'pause confirmed':
            self.confirmedPause.emit()



    def request_beam(self, polarity, charge):
        # ack for beam
        self.req_chan.setValue(cmd_text('request beam',
                                        {'name': self.name,
                                         'polarity': polarity,
                                         'charge': charge}))

    def reject_beam(self):
        # say that no beam needed
        self.req_chan.setValue(cmd_text('reject beam', {'name': self.name}))

    def pause_beam(self):
        # temporary pause beam
        self.req_chan.setValue(cmd_text('pause beam', {'name': self.name}))

    def continue_beam(self):
        # continue if paused before
        self.req_chan.setValue(cmd_text('continue beam', {'name': self.name}))

    def send_msg(self, msg_text):
        # continue if paused before
        self.req_chan.setValue(cmd_text('msg', {'name': self.name, 'msg_text': msg_text}))



class BeamUserSer(BeamUserBase):
    requestBeam = pyqtSignal(str, str, float)
    rejectBeam = pyqtSignal(str)
    pauseBeam = pyqtSignal(str)
    continueBeam = pyqtSignal(str)
    newMsg = pyqtSignal(str, str)

    def __init__(self, name, ctl_dev):
        super(BeamUserSer, self).__init__(name, ctl_dev)

    def req_cb(self, chan):
        try:
            cdict = json.loads(chan.val)
        except:
            return
        if cdict['cmd'] == 'request beam':
            self.requestBeam.emit(cdict['name'], cdict['polarity'], cdict['charge'])
        if cdict['cmd'] == 'reject beam':
            self.rejectBeam.emit(cdict['name'])
        if cdict['cmd'] == 'pause beam':
            self.pauseBeam.emit(cdict['name'])
        if cdict['cmd'] == 'continue beam':
            self.continueBeam.emit(cdict['name'])
        if cdict['cmd'] == 'msg':
            self.newMsg.emit(cdict['name'], cdict['msg_text'])
        chan.setValue('')

    def ans_cb(self, chan):
        # srv just send in this direction
        pass

    def deny_beam(self, reason):
        self.ans_chan.setValue(cmd_text('beam denied', {'name': self.name, 'reason': reason}))

    def accept_request(self):
        self.ans_chan.setValue(cmd_text('request accepted', {'name': self.name}))

    def confirm_reject(self):
        self.ans_chan.setValue(cmd_text('reject confirmed', {'name': self.name}))

    def confirm_pause(self):
        self.ans_chan.setValue(cmd_text('pause confirmed', {'name': self.name}))




