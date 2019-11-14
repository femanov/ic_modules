#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QBrush, QPen, QColor, QPainter
from PyQt5.QtCore import Qt, QRect
import PyQt5.QtGui as QtGui

class FSwitch(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setMinimumWidth(36)
        self.setMinimumHeight(18)

        self.pict = {}
        #self.generate_picts()

    def generate_pict(self, checked, size_x, size_y):
        pic = QtGui.QPicture()

        bg_color = Qt.green if checked else Qt.red

        radius = size_y/2
        center = self.rect().center()

        p = QtGui.QPainter(pic)
        p.setRenderHint(QPainter.Antialiasing)
        p.translate(center)
        p.setBrush(QColor(130,140,160))




    def paintEvent(self, event):
        label = "ON" if self.isChecked() else "OFF"
        bg_color = Qt.green if self.isChecked() else Qt.red

        radius = 7

        width = 22
        center = self.rect().center()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(QColor(130,140,160))

        pen = QPen(QColor(40,40,70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRoundedRect(QRect(-width, -radius, 2*width, 2*radius), radius, radius)
        painter.setBrush(QBrush(bg_color))
        sw_rect = QRect(-radius, -radius, width + radius, 2*radius)

        if not self.isChecked():
            sw_rect.moveLeft(-width)
        painter.drawRoundedRect(sw_rect, radius, radius)
        painter.drawText(sw_rect, Qt.AlignCenter, label)


if __name__ == '__main__':
    app = QApplication(['test switcher'])
    w = FSwitch()
    w.show()
    app.exec_()
