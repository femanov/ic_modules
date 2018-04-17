
from acc_db.db import *
from PyQt5 import QtGui, uic, QtCore
from PyQt5.QtWidgets import QTableWidgetItem
import fwidgets as fw

class KindTable(QtCore.QObject):
    def __init__(self, table_widget):
        super(QtCore.QObject, self).__init__()
        self.table_widget = table_widget
        self.table_widget.verticalHeader().setVisible(False)
        # database connect
        self.db = acc_db()
        self.cur = self.db.cur
        self.conn = self.db.conn

        self.db.execute("SELECT DISTINCT access from chan WHERE NOT access=\'p\'")
        self.conn.commit()
        self.kindlist = [x[0] for x in self.cur.fetchall()]
        self.checkers = []

        self.table_widget.setRowCount(len(self.kindlist))
        for ind in range(len(self.kindlist)):
            item = QTableWidgetItem(self.kindlist[ind])
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table_widget.setItem(ind, 0, item)
            self.checkers.append(fw.FCheckBox(self.table_widget))
            self.table_widget.setCellWidget(ind, 1, self.checkers[-1])
            if self.kindlist[ind] == 'rw':
                self.checkers[-1].setValue(1)

        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()


    def selected(self):
        res = []
        for ind in range(len(self.checkers)):
            if self.checkers[ind].isChecked():
                res.append(self.kindlist[ind])
        return res