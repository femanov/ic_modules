import daemon
import signal
import sys
import pid
import time

class Service:
    def __init__(self, name):
        self.name = name
        self.f_log = open('/var/tmp/' + self.name + '.log', 'ab', 0)
        self.f_err = open('/var/tmp/' + self.name + '.err', 'ab', 0)
        self.dcontext = daemon.DaemonContext(pidfile=pid.PidFile(self.name, '/var/tmp',),
                                        stdout=self.f_log,
                                        stderr=self.f_err)

        self.dcontext.signal_map = {
            signal.SIGTERM: self.exit_proc,
        }

        with self.dcontext:
            self.log_str('starting service: ' + self.name)
            self.pre_run()
            self.main()
            self.run_main_loop()

    def exit_proc(self, signum, frame):
        self.log_str('signal recieved: %d, %s' % (signum, frame))
        self.clean_proc()
        sys.stdout.flush()
        self.quit_main_loop()

    def log_str(self, msg):
        print(time.time(), ': ', msg)
        sys.stdout.flush()

    def run_main_loop(self):
        pass

    def quit_main_loop(self):
        pass

    def pre_run(self):
        #function to initialize context here
        pass

    def main(self):
        pass

    def clean_proc(self):
        pass


class QtService(Service):
    def __init__(self, name):
        self.app = None
        super(QtService, self).__init__(name)

    def pre_run(self):
        print('prerun')
        global QtCore
        import aQt.QtCore as QtCore

        self.app = QtCore.QCoreApplication(sys.argv)
        print(self.app)

    def run_main_loop(self):
        print('starting main loop')
        print(self.app)
        self.app.exec()


    def quit_main_loop(self):
        self.app.quit()



class CothreadQtService(Service):
    def __init__(self, name):
        self.app = None
        super(CothreadQtService, self).__init__(name)

    def run_main_loop(self):
        global cothread
        cothread.WaitForQuit()

    def quit_main_loop(self):
        self.app.quit()

    def pre_run(self):
        global QtCore, cothread
        from aQt import QtCore
        import cothread

        self.app = QtCore.QCoreApplication(sys.argv)
        cothread.iqt()


class CXService(Service):
    def run_main_loop(self):
        global cda
        import pycx4.pycda as cda
        cda.main_loop()

    def quit_main_loop(self):
        global cda
        import pycx4.pycda as cda
        cda.break_()

