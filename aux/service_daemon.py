import daemon
import signal
import sys
import pid


class Service(object):
    def __init__(self, name, main_proc, clean_proc=None):
        self.name, self.main_proc, self.clean_proc = name, main_proc, clean_proc
        self.f_log = open('/var/tmp/' + self.name + '.log', 'ab', 0)
        dcontext = daemon.DaemonContext(pidfile=pid.PidFile(self.name, '/var/tmp',),
                                        stdout=self.f_log,
                                        stderr=self.f_log)

        dcontext.signal_map = {
            signal.SIGTERM: self.exit_proc,
        }

        with dcontext:
            print('starting service: ' + self.name)
            sys.stdout.flush()
            self.main_proc()

    def exit_proc(self, signum, frame):
        print('signal recieved', signum, frame)
        sys.stdout.flush()
        if self.clean_proc is not None:
            self.clean_proc()


