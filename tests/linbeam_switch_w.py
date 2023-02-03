#!/usr/bin/env python3

from PyQt5.QtWidgets import QLabel, QLineEdit, QApplication
from cxwidgets.auxwidgets import BaseGridW
from cxwidgets import CXLineEdit, CXDevSwitch, CXStrLabel, CXIntLabel


class LinBeamStateWidget(BaseGridW):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.grid.addWidget(QLabel("Linac beam state:"), 0, 0)
        self.grid.addWidget(CXDevSwitch(devname='beamswitch'), 0, 1)

        self.beam_swc_state = CXIntLabel(cname='beamswitch.state',
                                        values={
                                            -2: 'failed',
                                            -1: 'unknown',
                                            0:  'off',
                                            1:  'on',
                                            2: 'turning_off',
                                            3: 'turning_on',
                                           },
                                        colors={
                                            -2: '#000099',
                                            -1: '#FFFFFF',
                                            0: '#FF0000',
                                            1: '#00FF00',
                                            2: '#FFFF00',
                                            3: '#FFFF00',
                                                })
        self.beam_swc_state.setMinimumWidth(80)
        self.grid.addWidget(self.beam_swc_state, 0, 2)


if __name__ == '__main__':
    app = QApplication(['mode list test'])

    w = LinBeamStateWidget()
    w.show()

    app.exec_()
