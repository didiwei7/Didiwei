import os
import sys
import os.path
os.chdir(os.path.split(os.path.realpath(__file__))[0])

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class QMySlider(QWidget):

    valueChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(QMySlider, self).__init__()
        self.parent = parent

        self.__label_name = QLabel()
        self.__label_value = QLabel()
        self.__slider = QSlider(Qt.Horizontal)

        self.__setupUi()

        with open("qmyslider.qss", "r") as file:
            self.setStyleSheet(file.read())

        # file = QFile("qmyslider.qss")
        # file.open(QIODevice.ReadOnly)
        # style = file.readAll()
        # self.setStyleSheet(str(style, encoding="utf-8"))

        self.__slider.valueChanged.connect(self.setLabelValue)

    def __setupUi(self):
        layout_1 = QVBoxLayout()
        layout_1.setContentsMargins(0, 0, 0, 0)
        layout_1.setSpacing(0)
        layout_2 = QHBoxLayout()
        layout_2.setContentsMargins(0, 0, 0, 0)
        layout_2.setSpacing(0)

        layout_2.addWidget(self.__label_name)
        layout_2.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout_2.addWidget(self.__label_value)

        layout_1.addLayout(layout_2)
        layout_1.addWidget(self.__slider)

        self.setLayout(layout_1)

        self.setMouseTracking(True)
        self.setFixedWidth(150)

    def setWidth(self, width):
        self.setFixedWidth(width)
        self.update()

    def setText(self, sname):
        self.__label_name.setText(sname)

    def setRange(self, min_value, max_value):
        self.__slider.setRange(min_value, max_value)

    def setPageStep(self, page_value):
        self.__slider.setPageStep(page_value)

    def setValue(self, value):
        self.__slider.setValue(value)
        self.__label_name.setText(str(value))

    def setLabelValue(self, value):
        self.__label_value.setText(str(value))
        self.valueChanged.emit(value)

    def currentValue(self):
        return self.__slider.value()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QMySlider()
    w.show()
    sys.exit(app.exec_())