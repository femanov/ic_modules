#!/usr/bin/env python3

from acc_db.db import *
from aux.Qt import QtGui, uic, QtCore, QtWidgets

import os

modpath = os.path.dirname(os.path.realpath(__file__))
print_selection = False


# some general tree implementation
# low performance but works for small trees
class Node(object):
    def __init__(self, parent, db_id, name, sord, widget):
        self.parent, self.db_id, self.name, self.sord, self.widget = parent, db_id, name, sord, widget
        self.children = []
        self.br_list = []
        if parent is not None:
            parent.add_child(self)

        self.selected = 0  # 0 - unselected, 1 - partial selection, 2 - selected

    def add_child(self, obj):
        self.children.append(obj)

    def nodeByWidget(self, w):
        for x in self.br_list:
            if x.widget == w:
                return x

    def nodeByIdPath(self, id_path):
        l = len(id_path)
        node = self
        for x in range(l):
            found = False
            for y in node.children:
                if id_path[x] == y.db_id:
                    node = y
                    found = True
                    break
            if not found:
                print('aaa!')
                print(id_path)
                raise(Exception('tree item not found'))
        return node

    def branch_list(self):
        br_list = []
        path_ord = [0]
        cNode = self
        level = 0
        # tree traversal loop
        while 1:
            # write current node
            br_list.append(cNode)
            # select next node
            if len(cNode.children) > 0:
                cNode = cNode.children[0]
                level += 1
                path_ord.append(0)
            else:
                if path_ord[-1] + 1 < len(cNode.parent.children) and level > 0:
                    path_ord[-1] += 1
                    cNode = cNode.parent.children[path_ord[-1]]
                else:
                    level_up_ok = False
                    while level > 1:
                        level -= 1
                        path_ord.pop(-1)
                        cNode = cNode.parent
                        if path_ord[-1] + 1 < len(cNode.parent.children):
                            path_ord[-1] += 1
                            cNode = cNode.parent.children[path_ord[-1]]
                            level_up_ok = True
                            break
                    if not level_up_ok:
                        break
        self.br_list = br_list

    def parents(self):
        cNode = self
        plist = []
        while cNode.parent is not None:
            cNode = cNode.parent
            plist.append(cNode)
        return plist

    def print_tree(self):
        pass


class DevTree(QtCore.QObject):

    def __init__(self, treeWidget, show_devs=True, show_unsorted=True):
        QtCore.QObject.__init__(self)
        self.tree = treeWidget

        self.icon_allow = QtGui.QIcon(modpath + '/img/icon_allow.jpg')
        self.icon_forbid = QtGui.QIcon(modpath + '/img/icon_forb.jpg')
        self.icon_part = QtGui.QIcon(modpath + '/img/icon_part.jpg')

        # database connect
        self.db = acc_db()
        self.cur = self.db.cur
        self.conn = self.db.conn

        self.db.execute('WITH RECURSIVE topsys AS ( '
                    '((select id, label, description, ord, array[id] as path from sys where parent_id is NULL )) '
                    'UNION ALL select sys.id, sys.label, sys.description, sys.ord, (topsys.path || sys.id) from topsys, sys '
                    'where sys.parent_id=topsys.id ) '
                    'select * from topsys order by ord;')
        self.conn.commit()
        self.syslist = self.cur.fetchall()

        self.ntree = Node(None, 0, 'tree', 0, self.tree)

        for x in self.syslist:
            p_ntree = self.ntree.nodeByIdPath(x[4][:len(x[4])-1])
            w = QtWidgets.QTreeWidgetItem(p_ntree.widget, [x[1]])
            w.setToolTip(0, x[2])
            w.setIcon(0, self.icon_forbid)
            Node(p_ntree, x[0], x[1], x[3], w)

        self.ntree.branch_list()


        if show_devs:
            for x in self.ntree.br_list:
                self.db.execute('select dev.id,dev.label from dev,sys_devs where '
                             'sys_devs.dev_id=dev.id and sys_devs.sys_id=%s ORDER BY dev.ord', (x.db_id,))
                self.conn.commit()
                devs = self.cur.fetchall()
                for y in devs:
                    QtWidgets.QTreeWidgetItem(x.widget, [y[1]])

        if show_unsorted:
            self.unsorted_w = QtWidgets.QTreeWidgetItem(self.tree, ["unsorted"])
            self.db.execute('select dev.id,dev.label from dev where'
                        ' not exists (select id from sys_devs where dev_id=dev.id)')
            self.conn.commit()
            devs = self.cur.fetchall()
            for y in devs:
                QtWidgets.QTreeWidgetItem(self.unsorted_w, [y[1]])

        self.tree.itemPressed.connect(self.itemSelect)

    def itemSelect(self, item_w, col):
        ntree = self.ntree
        node = ntree.nodeByWidget(item_w)
        if node is None:
            return
        parents = node.parents()
        parents.pop(-1)

        if node.selected == 0 or node.selected == 1:
            node.selected = 2
            item_w.setIcon(0, self.icon_allow)

            # parents traversal
            for x in parents:
                all_sel = True
                for y in x.children:
                    if y.selected != 2:
                        all_sel = False
                        break
                if all_sel:
                    x.selected = 2
                    x.widget.setIcon(0, self.icon_allow)
                else:
                    x.selected = 1
                    x.widget.setIcon(0, self.icon_part)

            # descendants traversal
            if not node.br_list:
                node.branch_list()
            for x in node.br_list:
                if x.selected != 2:
                    x.selected = 2
                    x.widget.setIcon(0, self.icon_allow)

        elif node.selected == 2:
            node.selected = 0
            item_w.setIcon(0, self.icon_forbid)

            # parents traversal
            for x in parents:
                children = x.children
                all_unsel = True
                for y in children:
                    if y.selected != 0:
                        all_unsel = False
                        break
                if all_unsel:
                    x.selected = 0
                    x.widget.setIcon(0, self.icon_forbid)
                else:
                    x.selected = 1
                    x.widget.setIcon(0, self.icon_part)

            # descendants traversal
            if not node.br_list:
                node.branch_list()
            for x in node.br_list:
                if x.selected != 0:
                    x.selected = 0
                    x.widget.setIcon(0, self.icon_forbid)
        if print_selection:
            tree_list = self.ntree.br_list
            syslist = [x.db_id for x in tree_list if x.selected == 2]
            print(syslist)


if __name__=='__main__':
    class MyWindow(QtWidgets.QMainWindow):
        def __init__(self):
            super(MyWindow, self).__init__()
            uic.loadUi('dev_tree.ui', self)
            self.show()

            self.dev_tree = DevTree(self.tree, True, True)

    print_selection = True
    app = QtWidgets.QApplication(['dev_tree'])
    win = MyWindow()
    app.exec_()
