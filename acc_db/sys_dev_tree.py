#!/usr/bin/env python3

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QApplication
from PyQt5.QtGui import QIcon

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
django.setup()

from accdb.models import Sys, Dev
modpath = os.path.dirname(os.path.realpath(__file__))

#states
UNSELECTED,SELECTED,PARTLY = 0,1,2

class SysDevTreeItem(QTreeWidgetItem):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self.db_name = kwargs.get('db_name', 'name')
        self.label = kwargs.get('label', self.db_name)
        self.db_type = kwargs.get('db_type', 'type')
        self.db_id = kwargs.get('db_id', 0)
        self.path = kwargs.get('path', "")
        self.description = kwargs.get('desc', '')
        self.setText(0,self.label)
        self.setToolTip(0, self.description)
        self.set_state(UNSELECTED)

    def set_state(self, state):
        self.state = state
        tree = self.treeWidget()
        self.setIcon(0, tree.sel_icons[self.db_type][state])
        selected_set = self.treeWidget().selected[self.db_type]
        if state == SELECTED:
            selected_set.add(self.db_id)
        elif self.db_id in selected_set:
            selected_set.remove(self.db_id)

    def update_state(self):
        c_selected = 0
        for i in range(self.childCount()):
            c = self.child(i)
            if c.state == SELECTED:
                c_selected += 1
            elif c.state == PARTLY:
                self.set_state(PARTLY)
                return
        else:
            if c_selected == self.childCount():
                self.set_state(SELECTED)
            elif c_selected > 0:
                self.set_state(PARTLY)
            else:
                self.set_state(UNSELECTED)

    def __str__(self):
        return "<SysDevTreeItem: name=" + self.db_name + " type=" + self.db_type + " id=" + str(self.db_id) + ">"

    def __hash__(self):
        return hash(id(self))


class SysTreeWidget(QTreeWidget):
    sysSelectionChanged = pyqtSignal(set)
    devsSelectionChanged = pyqtSignal(set)
    itemClicked = pyqtSignal(SysDevTreeItem)

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.show_devs = kwargs.get('show_devs', False)
        self.devs_select = kwargs.get('devs_select', False)
        self.top_id = kwargs.get('top_id', 0)
        self.show_unsorted = kwargs.get('show_unsorted', False)

        self.sel_icons = {
            'sys': {
                UNSELECTED: QIcon(modpath + '/img/icon_forb.jpg'),
                SELECTED: QIcon(modpath + '/img/icon_allow.jpg'),
                PARTLY: QIcon(modpath + '/img/icon_part.jpg')
            },
            'dev': {
                UNSELECTED: QIcon(modpath + '/img/dev_unsel.png'),
                SELECTED: QIcon(modpath + '/img/dev_sel.png'),
            }
        }

        self.db_tree = Sys.get_tree() if self.top_id == 0 else Sys.get_tree(parent=Sys.objects.get(pk=self.top_id))
        steplen = Sys.steplen
        top_depth = self.db_tree[0].depth

        self.path_id = {x.path: x.id for x in self.db_tree}

        self.selected = {'sys': set(),
                         'dev': set()}
        self.sys_id_ws = {}
        self.dev_id_ws = {}

        for x in self.db_tree:
            par = self if x.depth == top_depth else self.sys_id_ws[self.path_id[x.path[:-1*steplen]]]
            w = SysDevTreeItem(par, db_name=x.name, label=x.label, db_type='sys', db_id=x.id, path=x.path, desc=x.description)
            self.sys_id_ws[x.id] = w

            if self.show_devs:
                devs = x.devs.order_by('ord')
                for d in devs:
                    wd = SysDevTreeItem(w, db_name=d.name, label=d.label, db_type='dev', db_id=d.id, desc=d.description)
                    if d.id in self.dev_id_ws:
                        self.dev_id_ws[d.id].append(wd)
                    else:
                        self.dev_id_ws[d.id] = [wd]

        # this is for db check only, not working correct yet
        if self.show_devs and self.show_unsorted:
            w = SysDevTreeItem(self, db_name='unsorted', db_type='sys', db_id=0, desc='no any sys for this devs-+')
            unsorted_devs = Dev.objects.filter(sys__isnull=True)
            for d in unsorted_devs:
                SysDevTreeItem(w, db_name=d.name, label=d.label, db_type='dev', db_id=d.id, desc=d.description)

        self.itemPressed.connect(self.item_click_cb)
        self.header().hide()
        self.setSelectionMode(0)

    def item_click_cb(self, item_w, col):
        if item_w.state == SELECTED:
            self.set_item_state(item_w, UNSELECTED)
        else:
            self.set_item_state(item_w, SELECTED)
        self.sysSelectionChanged.emit(self.selected['sys'])
        self.devsSelectionChanged.emit(self.selected['dev'])
        self.itemClicked.emit(item_w)

    def set_item_state(self, item_w, state, update_anc=True, update_decs=True):
        if item_w.state == state:
            return None
        item_w.set_state(state)
        if update_anc:
            self.item_ancestors_selupdate(item_w)
        if item_w.db_type == 'dev':
            w_rels = set()
            for x in self.dev_id_ws[item_w.db_id]:
                if item_w == x:
                    continue
                x.set_state(state)
                if update_anc:
                    self.item_ancestors_selupdate(x)
                else:
                    w_rels.add(x)
            return w_rels
        else:
            if update_decs:
                self.item_desc_set_state(item_w, state)
        return None

    def item_ancestors_selupdate(self, item_w):
        p = item_w.parent()
        while p is not None:
            p.update_state()
            p = p.parent()

    def item_desc_set_state(self, item_w, state):
        nb_devs = set()
        brach_devs = set()
        pos = self.next_node(item_w, top=item_w)
        while pos is not None:
            ans = self.set_item_state(pos, state, update_anc=False, update_decs=False)
            if ans:
                nb_devs.update(ans)
            if pos.db_type == 'dev':
                brach_devs.add(pos)
            pos = self.next_node(pos, top=item_w)
        to_upd = nb_devs - brach_devs
        for x in to_upd:
            self.item_ancestors_selupdate(x)

    # to go around brunch, needed since sys and devs mixed
    def next_node(self, item_w, **kwargs):
        top = kwargs.get('top', None)
        if item_w.childCount() > 0:
            return item_w.child(0)
        else:
            par = item_w.parent()
            chi = item_w
            while par is not None:
                if par.childCount() > par.indexOfChild(chi) + 1:
                    return par.child(par.indexOfChild(chi) + 1)
                chi = par
                par = par.parent()
                if chi is top:
                    return None
            return None

if __name__=='__main__':
    app = QApplication(['dev_tree'])

    w = SysTreeWidget(show_devs=True, show_unsorted=True, top_id=0)
    w.resize(400, 800)
    w.show()
    w.sysSelectionChanged.connect(print)
    w.devsSelectionChanged.connect(print)
    w.itemClicked.connect(print)

    app.exec_()


