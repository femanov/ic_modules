#!/usr/bin/env python3

from cxwidgets.aQt import QtWidgets, QtCore
import pycx4.qcda as cda
import pyqtgraph as pg
import numpy as np
import sys
import time

class ChanHist:
    def __init__(self, cname, hist_time):
        self._cname, self._hist_time = cname, hist_time
        self.chan, self.ar_len, self.pos, self.used = None, 4096, 0, 0
        self.ar_inc = 4096

        self.data_v, self.data_t = np.zeros(self.ar_len), np.zeros(self.ar_len)
        self.cx_connect()

    def cx_connect(self):
        if self._cname is None:
            return
        self.chan = cda.DChan(self._cname, private=True, on_update=True)
        self.chan.valueMeasured.connect(self.cs_update)

    def cs_update(self, chan):
        if self.pos == 0:
            if self.used == 0:
                t_min = 0
            else:
                t_min = time.time() - self.data_t[1]
        else:
            t_min = time.time() - self.data_t[0]
        if self.ar_len <= self.pos and t_min < self._hist_time:
            self.ar_len += self.ar_inc
            self.data_v = np.resize(self.data_v, self.ar_len)
            self.data_t = np.resize(self.data_t, self.ar_len)
        if t_min >= self._hist_time:
            self.used = self.pos
            self.pos = 0
        self.data_v[self.pos] = chan.val
        self.data_t[self.pos] = chan.time / 1.e6
        self.pos += 1

    def _get_xy(self):
        cur_t = time.time()
        if self.used > 0:
            vals = np.roll(self.data_v[:self.used], -1 * self.pos)
            times = np.roll(self.data_t[:self.used], -1 * self.pos)
        else:
            vals = np.roll(self.data_v[:self.pos], -1 * self.pos)
            times = np.roll(self.data_t[:self.pos], -1 * self.pos)
        return times-cur_t, vals

    xy = property(_get_xy)


class CXHistPlot(pg.PlotWidget):
    def __init__(self, parent=None, backdround='default', **kwargs):
        super(CXHistPlot, self).__init__(parent, backdround, **kwargs)
        if 'cname' in kwargs:
            cname = kwargs['cname']
        else:
            cname = None
        if 'hist_time' in kwargs:
            self._hist_time = kwargs['hist_time']
        else:
            self._hist_time = 100

        self.setXRange(-1 * self._hist_time, 0)

        self.colors = ['#ff0000', '#00ff00', '#0000ff', '#ff00ff']
        self.cnames = []
        self.plts = []
        self.curvs = []
        self.hists = []

        if cname:
            self.addChan(cname)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.upd_plot)
        self.timer.start(1000)


    def upd_plot(self):
        for ind in range(len(self.cnames)):
            xy = self.hists[ind].xy
            self.curvs[ind].setData(y=xy[1], x=xy[0])

    def addChan(self, cname):
        # check length
        ind = len(self.cnames)
        self.cnames.append(cname)
        self.hists.append(ChanHist(cname, self._hist_time))
        if ind == 0:
            p = self.plotItem
            self.plts.append(p)
            c = self.plot(name=cname, pen=pg.mkPen(self.colors[ind]))
            p.getAxis('left').setLabel(cname, color=self.colors[ind])
            self.curvs.append(c)
            p.vb.sigResized.connect(self.updateviews)
        else:
            p = pg.ViewBox()
            ax = pg.AxisItem('right')
            self.plts[0].layout.addItem(ax, 2, 3+ind)
            self.plts[0].scene().addItem(p)
            ax.linkToView(p)
            p.setXLink(self.plts[0])
            ax.setZValue(-10000)

            ax.setLabel(cname, color=self.colors[ind])
            self.plts.append(p)
            c = pg.PlotCurveItem(name=cname, pen=pg.mkPen(self.colors[ind]))
            p.addItem(c)
            self.curvs.append(c)
        self.updateviews()

    def updateviews(self):
        for p in self.plts[1:]:
            p.setGeometry(self.plts[0].vb.sceneBoundingRect())
            p.linkedViewChanged(self.plts[0].vb, p.XAxis)


class CXHistPlot2(pg.GraphicsLayoutWidget):
    def __init__(self, parent=None, **kwargs):
        super(CXHistPlot2, self).__init__(parent, **kwargs)
        self.cnames = kwargs.get('cnames', None)
        self._hist_time = kwargs.get('hist_time', 100)
        # self.ci - central item = graphics layout
        # # layout next is a difference
        # l = pg.GraphicsLayout()
        # pw.setCentralWidget(l)

        #self.setXRange(-1 * self._hist_time, 0)

        self.colors = ['#ff0000', '#00ff00', '#0000ff', '#ff00ff']
        self.cnames = []
        self.plts = []
        self.curvs = []
        self.hists = []

        self.axs = []

        # if cname:
        #     self.addChan(cname)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.upd_plot)
        self.timer.start(1000)

        self.max_chans = 4



    def addChan(self, cname):
        pass

    # Axis
    a2 = pg.AxisItem("left")
    a3 = pg.AxisItem("left")
    a4 = pg.AxisItem("left")
    a5 = pg.AxisItem("left")
    a6 = pg.AxisItem("left")

    # ViewBoxes
    v2 = pg.ViewBox()
    v3 = pg.ViewBox()
    v4 = pg.ViewBox()
    v5 = pg.ViewBox()
    v6 = pg.ViewBox()


    # add axis to layout
    ## watch the col parameter here for the position
    l.addItem(a2, row=2, col=5, rowspan=1, colspan=1)
    l.addItem(a3, row=2, col=4, rowspan=1, colspan=1)
    l.addItem(a4, row=2, col=3, rowspan=1, colspan=1)
    l.addItem(a5, row=2, col=2, rowspan=1, colspan=1)
    l.addItem(a6, row=2, col=1, rowspan=1, colspan=1)

    # plotitem and viewbox
    ## at least one plotitem is used whioch holds its own viewbox and left axis
    pI = pg.PlotItem()
    v1 = pI.vb  # reference to viewbox of the plotitem
    l.addItem(pI, row=2, col=6, rowspan=1, colspan=1)  # add plotitem to layout

    # add viewboxes to layout
    l.scene().addItem(v2)
    l.scene().addItem(v3)
    l.scene().addItem(v4)
    l.scene().addItem(v5)
    l.scene().addItem(v6)

    # link axis with viewboxes
    a2.linkToView(v2)
    a3.linkToView(v3)
    a4.linkToView(v4)
    a5.linkToView(v5)
    a6.linkToView(v6)

    # link viewboxes
    v2.setXLink(v1)
    v3.setXLink(v2)
    v4.setXLink(v3)
    v5.setXLink(v4)
    v6.setXLink(v5)

    # axes labels
    pI.getAxis("left").setLabel('axis 1 in ViewBox of PlotItem', color='#FFFFFF')
    a2.setLabel('axis 2 in Viewbox 2', color='#2E2EFE')
    a3.setLabel('axis 3 in Viewbox 3', color='#2EFEF7')
    a4.setLabel('axis 4 in Viewbox 4', color='#2EFE2E')
    a5.setLabel('axis 5 in Viewbox 5', color='#FFFF00')
    a6.setLabel('axis 6 in Viewbox 6', color='#FE2E64')

    # slot: update view when resized
    def updateViews():
        v2.setGeometry(v1.sceneBoundingRect())
        v3.setGeometry(v1.sceneBoundingRect())
        v4.setGeometry(v1.sceneBoundingRect())
        v5.setGeometry(v1.sceneBoundingRect())
        v6.setGeometry(v1.sceneBoundingRect())





app = QtWidgets.QApplication(sys.argv)


# plt = pg.plot(np.random.normal(size=100), title="Simplest possible plotting example")
# print(plt)
w = CXHistPlot(cname='sled1.Imes', hist_time=5000)
#w.addChan('WG4_2.Imes')

w.show()


sys.exit(app.exec_())
