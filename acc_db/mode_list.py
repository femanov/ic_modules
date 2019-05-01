#!/usr/bin/env python3

import math
from aux.Qt import QtGui, QtCore, QtWidgets
from fwidgets.auxwidgets import BaseGridW
from fwidgets.fspinbox import FSpinBox

from acc_db.db import ModesDB
from aux import str2u
from acc_ctl.mode_defs import mode_colors  # , rev_mode_map, mode_map

def_qcolor = QtGui.QColor("#fafafa")
mode_qcolors = {key: QtGui.QColor(mode_colors[key]) for key in mode_colors}
mode_dqcolors = {key: mode_qcolors[key].darker() for key in mode_qcolors}

# later may be use django ORM
# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
# django.setup()
#
# from accmode.models import Mode,ModeMark

class ModeList(QtWidgets.QTableWidget):
    modeSelected = QtCore.pyqtSignal(int)
    modeUpdated = QtCore.pyqtSignal()

    def __init__(self, parent=None, **kwargs):
        super(ModeList, self).__init__(parent)
        self.modes_db = kwargs.get('db', ModesDB())

        self.selected_row = None
        self.modes = None
        self.marked_modes = None
        self.all_modes = None

        self.cellClicked.connect(self.mode_select)
        self.cellChanged.connect(self.item_edit_proc)
        self.updating_list = False

        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.setColumnCount(5)
        self.setColumnWidth(0, 130)
        self.setColumnWidth(1, 400)
        self.setColumnWidth(2, 220)
        self.setColumnWidth(3, 60)
        self.setColumnWidth(4, 60)

        self.update_modelist(update_marked=True)

        self.background_color = self.item(0, 0).background()
        self.selected_color = QtGui.QColor(200, 255, 255)

    def item_edit_proc(self, row, col):
        if self.updating_list or col > 1:
            return
        c_text = self.item(row, col).text()
        if c_text != self.all_modes[row][col+1]:
            if col == 0:
                self.modes_db.update_mode(self.all_modes[row][0], author=c_text)
            if col == 1:
                self.modes_db.update_mode(self.all_modes[row][0], comment=c_text)
            self.all_modes[row][col+1] = c_text
            self.modeUpdated.emit()

    def update_modelist(self, **kwargs):
        self.updating_list = True
        limit = kwargs.get('limit', 100)
        offset = kwargs.get('offset', 0)
        update_marked = kwargs.get('update_marked', False)
        filter = kwargs.get('filter', None)
        load_archived = kwargs.get('load_archived', False)

        if update_marked:
            self.marked_modes = [list(x) for x in self.modes_db.marked_modes([1, 2, 3, 4, 5, 6, 7, 8])]

        self.modes = [list(x) for x in self.modes_db.mode_list(limit, offset, filter, load_archived)]

        self.all_modes = self.marked_modes + self.modes
        self.setRowCount(len(self.all_modes))
        for ind in range(len(self.all_modes)):
            row = self.all_modes[ind]
            for rind in range(1, len(row)):
                if rind == 3:
                    rtext = row[rind].strftime("%Y-%m-%d %H:%M:%S")
                else:
                    rtext = row[rind]
                item = QtWidgets.QTableWidgetItem(rtext)
                #item.setFlags(QtCore.Qt.ItemIsEditable)
                self.setItem(ind, rind-1, item)
                if rind == 4:
                    item.setBackground(mode_dqcolors.get(rtext, def_qcolor))
                if rind == 5:
                    item.setBackground(mode_qcolors.get(rtext, def_qcolor))

        self.resizeRowsToContents()

        self.selected_row = None
        self.updating_list = False

    def mode_select(self, row, col):
        if self.selected_row is not None:
            self.item(self.selected_row, 0).setBackground(self.background_color)
            self.item(self.selected_row, 1).setBackground(self.background_color)
            self.item(self.selected_row, 2).setBackground(self.background_color)
        self.selected_row = row
        self.item(row, 0).setBackground(self.selected_color)
        self.item(row, 1).setBackground(self.selected_color)
        self.item(row, 2).setBackground(self.selected_color)
        self.modeSelected.emit(self.all_modes[row][0])


class ModeListFilter(BaseGridW):
    # limit, offset, search
    ctrlsUpdate = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        super(ModeListFilter, self).__init__(parent)

        self.grid.addWidget(QtWidgets.QLabel("search"), 0, 0)

        self.filter_line = QtWidgets.QLineEdit()
        self.grid.addWidget(self.filter_line, 0, 1, 1, 6)
        self.filter_line.editingFinished.connect(self.filter_cb)

        self.prev_b = QtWidgets.QPushButton("<<")
        self.grid.addWidget(self.prev_b, 1, 0)
        self.prev_b.clicked.connect(self.prev_cb)

        self.nrows_box = FSpinBox()
        self.grid.addWidget(self.nrows_box, 1, 1)
        self.nrows_box.done.connect(self.nrows_cb)

        self.grid.addWidget(QtWidgets.QLabel("@"), 1, 2)

        self.startrow_box = FSpinBox()
        self.grid.addWidget(self.startrow_box, 1, 3)
        self.startrow_box.done.connect(self.startrow_cb)

        self.grid.addWidget(QtWidgets.QLabel("of"), 1, 4)

        self.maxrows_box = FSpinBox()
        self.grid.addWidget(self.maxrows_box, 1, 5)
        self.maxrows_box.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.maxrows_box.setReadOnly(True)

        self.next_b = QtWidgets.QPushButton(">>")
        self.grid.addWidget(self.next_b, 1, 6)
        self.next_b.clicked.connect(self.next_cb)

        self.nrows = 0
        self.maxrows = 0
        self.startrow = 0
        self.filter = ''

    def set_maxrows(self, maxrows):
        # really some validation needed, but let's assume maxrows always increasing
        self.maxrows = maxrows
        self.maxrows_box.setValue(maxrows)

    def set_nrows(self, nrows):
        self.nrows = nrows
        self.nrows_box.setValue(self.nrows)

    def nrows_cb(self, nrows):
        if self.startrow + nrows > self.maxrows:
            self.nrows = self.maxrows - self.startrow
            self.nrows_box.setValue(self.nrows)
        else:
            self.nrows = nrows
        self.send_vals()

    def startrow_cb(self, startrow):
        if self.nrows + startrow > self.maxrows:
            self.startrow = self.maxrows - self.nrows
            self.startrow_box.setValue(self.startrow)
        else:
            self.startrow = startrow
            self.send_vals()

    def filter_cb(self):
        self.filter = self.filter_line.text()
        if self.filter == "":
            self.filter = None
        self.send_vals()

    def prev_cb(self):
        if self.startrow - self.nrows >= 0:
            self.startrow -= self.nrows
        else:
            self.startrow = 0
        self.startrow_box.setValue(self.startrow)
        self.send_vals()

    def next_cb(self):
        if self.startrow + 2 * self.nrows < self.maxrows:
            self.startrow += self.nrows
        else:
            self.startrow = self.maxrows - self.nrows
        self.startrow_box.setValue(self.startrow)
        self.send_vals()

    def send_vals(self):
        self.ctrlsUpdate.emit(self.vals())

    def vals(self):
        return({'limit': self.nrows,
                'offset': self.startrow,
                'filter': self.filter})


class ModeListBControls(BaseGridW):
    mark = QtCore.pyqtSignal(str)
    load = QtCore.pyqtSignal()
    archive = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(ModeListBControls, self).__init__(parent)

        self.grid.addWidget(QtWidgets.QLabel("mark"), 0, 0, 2, 1)

        self.buttons = []
        self.marks = ['einj', 'eext', 'pinj', 'pext', 'e2v4', 'p2v4', 'e2v2', 'p2v2']
        m_len = len(self.marks)
        rlen = 4
        crow = 0
        for ind in range(m_len):
            if ind == rlen:
                crow += 1
            btn = QtWidgets.QPushButton(self.marks[ind])
            btn.setStyleSheet("background-color: " + mode_colors[self.marks[ind]])
            btn.setFixedWidth(100)
            self.grid.addWidget(btn, crow, ind - crow * rlen + 1)
            self.buttons.append(btn)
            btn.clicked.connect(self.buttons_cb)

        hSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.grid.addItem(hSpacer, 0, rlen + 2)

        self.btn_archive = QtWidgets.QPushButton('Archive')
        self.grid.addWidget(self.btn_archive, 0, rlen + 3)
        self.btn_archive.setStyleSheet("background-color: red")
        self.btn_archive.setFixedWidth(110)
        self.btn_archive.clicked.connect(self.archive)

        self.btn_load = QtWidgets.QPushButton('Load')
        self.grid.addWidget(self.btn_load, 0, rlen + 4)
        self.btn_load.setFixedWidth(110)
        self.btn_load.clicked.connect(self.load)

    def buttons_cb(self):
        ind = self.buttons.index(self.sender())
        self.mark.emit(self.marks[ind])


class ModeListSaveBlock(BaseGridW):
    saveMode = QtCore.pyqtSignal(str, str)
    outMsg = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(ModeListSaveBlock, self).__init__(parent)

        self.grid.addWidget(QtWidgets.QLabel("Comment:"), 0, 0)
        self.grid.addWidget(QtWidgets.QLabel("author:"), 1, 0)

        self.comment_line = QtWidgets.QLineEdit()
        self.grid.addWidget(self.comment_line, 0, 1)

        self.author_line = QtWidgets.QLineEdit()
        self.grid.addWidget(self.author_line, 1, 1)

        self.btn_save = QtWidgets.QPushButton('save')
        self.grid.addWidget(self.btn_save, 0, 2, 2, 1)
        self.btn_save.clicked.connect(self.save_cb)

    def save_cb(self):
        comment = str2u(self.comment_line.text())
        if len(comment) == 0:
            self.outMsg.emit('no comment - no save')
            return
        author = str2u(self.author_line.text())
        if len(author) == 0:
            self.outMsg.emit('save: it isn`t polite to operate machine anonymously')
            return
        self.saveMode.emit(author, comment)


class ModeListFull(BaseGridW):
    markMode = QtCore.pyqtSignal(int, str, str, str)  # mode_id, mark_id
    saveMode = QtCore.pyqtSignal(str, str)  # author, comment
    outMsg = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(ModeListFull, self).__init__(parent)
        self.modes_db = ModesDB()

        self.filterw = ModeListFilter()
        self.grid.addWidget(self.filterw, 0, 0)
        self.update_modenum()
        self.filterw.set_nrows(100)
        self.filterw.ctrlsUpdate.connect(self.filter_cb)

        self.listw = ModeList(db=self.modes_db)
        self.grid.addWidget(self.listw, 1, 0)
        self.listw.modeSelected.connect(self.mode_sel_cb)

        self.ctrlw = ModeListBControls()
        self.grid.addWidget(self.ctrlw, 2, 0)

        self.save_blk = ModeListSaveBlock()
        self.grid.addWidget(self.save_blk, 3, 0)
        self.save_blk.saveMode.connect(self.saveMode)
        self.save_blk.outMsg.connect(self.outMsg)

        self.selected_mode = None

    def filter_cb(self, args):
        self.listw.update_modelist(**args)

    def mode_sel_cb(self, mode_id):
        if self.selected_mode is None and mode_id > 0:
            self.ctrlw.mark.connect(self.mark_cb)
        self.selected_mode = mode_id

    def mark_cb(self, mark):
        self.markMode.emit(self.selected_mode, mark, 'saver', 'automatic mode')

    def update_modenum(self):
        self.modes_db.execute("select count(id) from mode")
        m_num = self.modes_db.cur.fetchall()[0][0]
        self.filterw.set_maxrows(m_num)

    def update_modelist(self, update_marked=False):
        fvals = self.filterw.vals()
        if update_marked:
            fvals['update_marked'] = True
        self.listw.update_modelist(**fvals)


if __name__ == '__main__':
    app = QtWidgets.QApplication(['mode_list'])

    # w = ModeList()
    # w.resize(800, 800)
    # w.show()
    # w.modeSelected.connect(print)

    # w1 = ModeListFilter()
    # w1.show()

    # w2 = ModeListBControls()
    # w2.show()
    # w2.markMode.connect(print)

    w3 = ModeListFull()
    w3.resize(900, 800)
    w3.show()
    w3.markMode.connect(print)


    app.exec_()
