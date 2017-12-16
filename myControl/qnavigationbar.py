import os
import sys
import os.path

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class QHNavigationBar(QWidget):

    currentItemChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(QHNavigationBar, self).__init__()
        self.parent = parent

        self.currentIndex = 0
        self.columnWidth = 80

        self.color_background = "#E4E4E4"
        self.color_selected = "#2CA7F8"

        self.color_pen_background = "#202020"
        self.color_pen_selected = "#FFFFFF"

        self.listItems = []

        self.setMouseTracking(True)
        self.setFixedHeight(30)

    def addItem(self, title):
        self.listItems.append(title)
        self.update()

    def setHeight(self, height):
        self.setFixedHeight(height)
        self.update()

    def setColumnWidth(self, col_width):
        self.columnWidth = col_width
        self.update()

    def setPenColorBackground(self, color):
        self.color_pen_background = color
        self.update()

    def setPenColorSelected(self, color):
        self.color_pen_selected = color
        self.update()

    def setColorBackground(self, color):
        self.color_background = color
        self.update()

    def setColorSelected(self, color):
        self.color_selected = color
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(self.color_background))
        painter.drawRect(self.rect())

        count = 0
        for str in self.listItems:
            itemPath = QPainterPath()
            itemPath.addRect(QRectF(count * self.columnWidth, 0, self.columnWidth, self.height()))

            if self.currentIndex == count:
                painter.setPen(QColor(self.color_pen_selected))
                painter.fillPath(itemPath, QColor(self.color_selected))
            else:
                painter.setPen(QColor(self.color_pen_background))
                painter.fillPath(itemPath, QColor(self.color_background))

            painter.drawText(QRect(count*self.columnWidth, 0, self.columnWidth, self.height()), Qt.AlignVCenter | Qt.AlignHCenter, str)

            count = count + 1

    def mousePressEvent(self, e):
        if e.x() / self.columnWidth < len(self.listItems):
            self.currentIndex = int(e.x() / self.columnWidth)
            self.currentItemChanged.emit(self.currentIndex)
            self.update()

class QVNavigationBar(QWidget):

    currentItemChanged = pyqtSignal(int)

    def __init__(self):
        super(QVNavigationBar, self).__init__()

        self.currentIndex = 0
        self.rowHeight = 40

        self.color_background = "#E4E4E4"
        self.color_selected = "#2CA7F8"

        self.color_pen_background = "#202020"
        self.color_pen_selected = "#FFFFFF"

        self.listItems = []

        self.setMouseTracking(True)
        self.setFixedWidth(120)

    def addItem(self, title):
        self.listItems.append(title)
        self.update()

    def setWidth(self, width):
        self.setFixedWidth(width)
        self.update()

    def setRowHeight(self, row_height):
        self.rowHeight = row_height
        self.update()

    def setPenColorBackground(self, color):
        self.color_pen_background = color
        self.update()

    def setPenColorSelected(self, color):
        self.color_pen_selected = color
        self.update()

    def setColorBackground(self, color):
        self.color_background = color
        self.update()

    def setColorSelected(self, color):
        self.color_selected = color
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(self.color_background))
        painter.drawRect(self.rect())

        count = 0
        for str in self.listItems:
            itemPath = QPainterPath()
            itemPath.addRect(QRectF(0, count * self.rowHeight, self.width(), self.rowHeight))

            if self.currentIndex == count:
                painter.setPen(QColor(self.color_pen_selected))
                painter.fillPath(itemPath, QColor(self.color_selected))
            else:
                painter.setPen(QColor(self.color_pen_background))
                painter.fillPath(itemPath, QColor(self.color_background))

            painter.drawText(QRect(0, count * self.rowHeight, self.width(), self.rowHeight), Qt.AlignVCenter | Qt.AlignHCenter, str)
            count = count + 1

    def mousePressEvent(self, e):
        if e.y() / self.rowHeight < len(self.listItems):
            self.currentIndex = int(e.y() / self.rowHeight)
            self.currentItemChanged.emit(self.currentIndex)
            self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QHNavigationBar()
    w.show()
    sys.exit(app.exec_())