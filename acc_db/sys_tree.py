#!/usr/bin/env python3
#from aux.Qt import QtGui, QtCore, QtWidgets

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QApplication
from PyQt5.QtGui import QIcon

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
django.setup()

from accdb.models import Sys, Dev

modpath = os.path.dirname(os.path.realpath(__file__))

class SysTree(QTreeWidget):
    selectionChanged = pyqtSignal(list)

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)

        self.show_devs = kwargs.get('show_devs', False)
        self.devs_select = kwargs.get('devs_select', False)
        self.top_id = kwargs.get('top_id', 0)
        self.show_unsorted = kwargs.get('show_unsorted', False)

        self.sel_icons = {
            0: QIcon(modpath + '/img/icon_forb.jpg'),
            1: QIcon(modpath + '/img/icon_part.jpg'),
            2: QIcon(modpath + '/img/icon_allow.jpg')
        }

        self.db_tree = Sys.get_tree() if self.top_id == 0 else Sys.get_tree(parent=Sys.objects.get(pk=self.top_id))
        self.steplen = Sys.steplen

        self.path_id = {x.path: x.id for x in self.db_tree}
        self.id_tpath = {x.id: x.path for x in self.db_tree}
        self.id_tree = {x.id: x for x in self.db_tree}

        self.id_path = {k: [self.path_id[x] for x in self.item_ancestors_path(v)] for (k, v) in self.id_tpath.items()}

        self.selection = {x.id: 0 for x in self.db_tree}

        self.id_ws = {}

        for x in self.db_tree:
            if len(self.id_path[x.id]) == 0:
                parent = self
            else:
                parent = self.id_ws[self.id_path[x.id][-1]]

            w = QTreeWidgetItem(parent, [x.name])

            self.id_ws[x.id] = w
            w.setIcon(0, self.sel_icons[0])
            w.setToolTip(0, x.description)

            if self.show_devs:
                devs = x.devs.all()
                for d in devs:
                    wd = QTreeWidgetItem(w, [d.name])
                    wd.setToolTip(0, d.description)

        if self.show_devs and self.show_unsorted:
            w = QTreeWidgetItem(self, ['unsorted_devs'])
            unsorted_devs = Dev.objects.filter(sys__isnull=True)
            for d in unsorted_devs:
                wd = QTreeWidgetItem(w, [d.name])
                wd.setToolTip(0, d.description)

        self.itemPressed.connect(self.item_click_cb)

        # 2DO: add processing for show devises

        self.header().hide()
        self.setSelectionMode(0)

    def selected_ids(self):
        return [k for k in self.selection if self.selection[k] == 2]

    def item_click_cb(self, item_w, col):
        sid = self.id_by_widget(item_w)
        if sid is None:
            return
        dpath = self.id_path[sid] + [sid]
        descend = [k for (k, v) in self.id_path.items() if v[:len(dpath)] == dpath]
        anc = reversed(self.id_path[sid])

        if self.selection[sid] == 0:
            self.set_item_selection(sid, 2)
            for x in descend:
                self.set_item_selection(x, 2)
            part_sel = False
            for x in anc:
                if part_sel:
                    self.set_item_selection(x, 1)
                    continue
                if self.id_tree[x].numchild == 1:
                    self.set_item_selection(x, 2)
                    continue
                lpath = self.id_path[x] + [x]
                for (k, v) in self.id_path.items():
                    if v == lpath and self.selection[k] < 2:
                        self.set_item_selection(x, 1)
                        part_sel = True
                        break
                if not part_sel:
                    self.set_item_selection(x, 2)
        else:
            self.set_item_selection(sid, 0)
            for x in descend:
                self.set_item_selection(x, 0)
            part_sel = False
            for x in anc:
                if part_sel:
                    self.set_item_selection(x, 1)
                    continue
                if self.id_tree[x].numchild == 1:
                    self.set_item_selection(x, 0)
                    continue
                lpath = self.id_path[x] + [x]
                for (k, v) in self.id_path.items():
                    if v == lpath and self.selection[k] > 0:
                        self.set_item_selection(x, 1)
                        part_sel = True
                        break
                if not part_sel:
                    self.set_item_selection(x, 0)
        self.selectionChanged.emit(self.selected_ids())

    def set_item_selection(self, sid, sel):
        self.selection[sid] = sel
        self.id_ws[sid].setIcon(0, self.sel_icons[sel])

    def item_ancestors_path(self, path):
        return [path[:(x+1)*self.steplen] for x in range(int(len(path)/self.steplen) - 1)]

    def item_descendants_path(self, path):
        return [x.path for x in self.db_tree if x.path.startswith(path) and len(x.path) > len(path)]

    def id_by_widget(self, w):
        for key in self.id_ws:
            if self.id_ws[key] == w:
                return key
        return None


class SysTree2(QTreeWidget):
    selectionChanged = pyqtSignal(list)

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)

        self.top_id = kwargs.get('top_id', 0)
        self.show_unsorted = kwargs.get('show_unsorted', False)

        self.sel_icons = {
            0: QIcon(modpath + '/img/icon_forb.jpg'),
            1: QIcon(modpath + '/img/icon_part.jpg'),
            2: QIcon(modpath + '/img/icon_allow.jpg')
        }

        self.db_tree = Sys.get_tree() if self.top_id == 0 else Sys.get_tree(parent=Sys.objects.get(pk=self.top_id))
        self.steplen = Sys.steplen

        self.path_id = {x.path: x.id for x in self.db_tree}
        self.id_tpath = {x.id: x.path for x in self.db_tree}
        self.id_tree = {x.id: x for x in self.db_tree}

        self.id_path = {k: [self.path_id[x] for x in self.item_ancestors_path(v)] for (k, v) in self.id_tpath.items()}

        self.sys_devs = {x.id:x.devs.all() for x in self.db_tree}

        self.sel_sys = {x.id: 0 for x in self.db_tree}
        self.sel_devs = set()

        self.id_ws = {}

        for x in self.db_tree:
            if len(self.id_path[x.id]) == 0:
                parent = self
            else:
                parent = self.id_ws[self.id_path[x.id][-1]]

            w = QTreeWidgetItem(parent, [x.name])

            self.id_ws[x.id] = w
            w.setIcon(0, self.sel_icons[0])
            w.setToolTip(0, x.description)

            if self.show_devs:
                devs = x.devs.all()
                for d in devs:
                    wd = QTreeWidgetItem(w, [d.name])
                    wd.setToolTip(0, d.description)

        if self.show_devs and self.show_unsorted:
            w = QTreeWidgetItem(self, ['unsorted_devs'])
            unsorted_devs = Dev.objects.filter(sys__isnull=True)
            for d in unsorted_devs:
                wd = QTreeWidgetItem(w, [d.name])
                wd.setToolTip(0, d.description)

        self.itemPressed.connect(self.item_click_cb)

        # 2DO: add processing for show devises

        self.header().hide()
        self.setSelectionMode(0)

    def selected_ids(self):
        return [k for k in self.selection if self.selection[k] == 2]

    def item_click_cb(self, item_w, col):
        sid = self.id_by_widget(item_w)
        if sid is None:
            return
        dpath = self.id_path[sid] + [sid]
        descend = [k for (k, v) in self.id_path.items() if v[:len(dpath)] == dpath]
        anc = reversed(self.id_path[sid])

        if self.selection[sid] == 0:
            self.set_item_selection(sid, 2)
            for x in descend:
                self.set_item_selection(x, 2)
            part_sel = False
            for x in anc:
                if part_sel:
                    self.set_item_selection(x, 1)
                    continue
                if self.id_tree[x].numchild == 1:
                    self.set_item_selection(x, 2)
                    continue
                lpath = self.id_path[x] + [x]
                for (k, v) in self.id_path.items():
                    if v == lpath and self.selection[k] < 2:
                        self.set_item_selection(x, 1)
                        part_sel = True
                        break
                if not part_sel:
                    self.set_item_selection(x, 2)
        else:
            self.set_item_selection(sid, 0)
            for x in descend:
                self.set_item_selection(x, 0)
            part_sel = False
            for x in anc:
                if part_sel:
                    self.set_item_selection(x, 1)
                    continue
                if self.id_tree[x].numchild == 1:
                    self.set_item_selection(x, 0)
                    continue
                lpath = self.id_path[x] + [x]
                for (k, v) in self.id_path.items():
                    if v == lpath and self.selection[k] > 0:
                        self.set_item_selection(x, 1)
                        part_sel = True
                        break
                if not part_sel:
                    self.set_item_selection(x, 0)
        self.selectionChanged.emit(self.selected_ids())

    def set_item_selection(self, sid, sel):
        self.selection[sid] = sel
        self.id_ws[sid].setIcon(0, self.sel_icons[sel])

    def item_ancestors_path(self, path):
        return [path[:(x+1)*self.steplen] for x in range(int(len(path)/self.steplen) - 1)]

    def item_descendants_path(self, path):
        return [x.path for x in self.db_tree if x.path.startswith(path) and len(x.path) > len(path)]

    def id_by_widget(self, w):
        for key in self.id_ws:
            if self.id_ws[key] == w:
                return key
        return None




if __name__=='__main__':
    app = QApplication(['dev_tree'])
    w = SysTree(show_devs=True)
    w.resize(400, 800)
    w.show()
    w.selectionChanged.connect(print)

    app.exec_()

