
# from PyQt5.QtCore import pyqtSignal
from beamctl.beamuser import BeamUserSer


class BeamScheduler:
    def __init__(self):
        # registering beam users
        self.users = {
            'vepp4':  BeamUserSer('vepp4', 'ichw1-2:0.vepp4'),
            'vepp2k': BeamUserSer('vepp2k', 'ichw1-2:0.vepp2k')
        }

        self.requests = {'vepp4':  None,
                         'vepp2k': None
                         }
        # connecting user signals
        for k in self.users:
            user = self.users[k]
            user.requestBeam.connect(self.beam_requested)
            user.rejectBeam.connect(self.beam_rejected)
            user.pauseBeam.connect(self.beam_paused)
            user.continueBeam.connect(self.beam_continued)
            user.newMsg.connect(self.new_msg)
            self.requests[k] = None

        self.priority = 'vepp4'
        self.processing = None
        self.current_user = None
        self.current_particles = None
        self.paused = False


    def beam_requested(self, name, polarity, charge):
        if charge <= 0.0:
            self.users[name].deny_beam('too low charge requested')
            return
        if self.processing == name:
            self.users[name].deny_beam('no changes while processing')
            return
        self.requests[name] = {'polarity': polarity,
                               'charge': charge}
        self.users[name].accept_request()
        if self.processing is None:
            self.next_user()
        # add code to start running if needed
        print(name, polarity, charge)

    def beam_rejected(self, name):
        if self.requests[name] is not None:
            self.requests[name] = None  # cancel future requests
        if self.processing == name:
            self.processing = None
            self.next_user()
        self.users[name].confirm_reject()
        print(name, 'beam rejected')

    def beam_paused(self, name):
        if not self.paused and self.processing == name:
            self.paused = True
            self.pause_beam()
            self.users[name].confirm_pause()
        print(name, 'beam paused')

    def beam_continued(self, name):
        print(name, 'beam continued')

    def new_msg(self, name, msg_text):
        print(name, msg_text)

    def next_user(self):
        # next user is called when processing is None
        if self.priority is not None:
            if self.requests[self.priority] is not None:
                self.run_beam(self.priority, self.requests[self.priority])
                return
        for k in self.requests:
            if self.requests[k] is not None:
                self.run_beam(k, self.requests[k])

    # --- interface to beam control

    def run_beam(self, user, request):
        self.processing = user
        print('running', user, request)
        # code to run here

    def stop_beam(self):
        pass

    def pause_beam(self):
        pass