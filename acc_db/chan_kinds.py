#!/usr/bin/env python3

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import fwidgets as fw

from acc_db.db import AccConfig


class KindTable(QTableWidget):
    selectionChanged = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(KindTable, self).__init__(parent)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)

        # database connect
        self.db = AccConfig()
        self.kinds = self.db.savable_access_kinds()
        self.checkers = []

        self.setRowCount(len(self.kinds))
        self.setColumnCount(2)
        for ind in range(len(self.kinds)):
            item = QTableWidgetItem(self.kinds[ind])
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.setItem(ind, 0, item)
            self.checkers.append(fw.FCheckBox(self))
            self.setCellWidget(ind, 1, self.checkers[-1])
            if self.kinds[ind] == 'rw':
                self.checkers[-1].setValue(1)
            self.checkers[-1].done.connect(self.update_selection)

        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def selected(self):
        return [self.kinds[ind] for ind in range(len(self.kinds)) if self.checkers[ind].isChecked()]

    def update_selection(self, val=None):
        self.selectionChanged.emit(self.selected())


if __name__ == '__main__':
    app = QtWidgets.QApplication(['dev_tree'])
    w = KindTable()
    w.resize(400, 800)
    w.show()
    w.selectionChanged.connect(print)

    app.exec_()



