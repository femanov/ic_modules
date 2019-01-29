# auxiliary widgets common for some programs

from aQt.QtWidgets import QWidget, QGridLayout, QFrame


class Line(QFrame):
    def __init__(self, *args):
        super(Line, self).__init__(*args)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(3)
        self.setMidLineWidth(3)


class BaseGridW(QWidget):
    def __init__(self, parent=None):
        super(BaseGridW, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(1)
        self.setLayout(self.grid)

