# -*- coding: utf-8 -*-

import os
import sys
import os.path
os.chdir(os.path.split(os.path.realpath(__file__))[0])
sys.path.append("db")
sys.path.append("ui")
sys.path.append("qss")
sys.path.append("res")

from myControl.qnavigationbar import *

from ui.ui_player import *
from ui.ui_playlist import *
from ui.ui_locallist import *
from ui.ui_searchedlist import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ui_mainwindow(QMainWindow):

    def __init__(self):
        super(ui_mainwindow, self).__init__()
 
        self.setupUi()
        self.connect_signals_slots()

    def setupUi(self):
        self.set_navigationBar()
        self.set_layout()

        self.setGeometry(QApplication.desktop().availableGeometry().adjusted(200, 200, -200, -200))

    def connect_signals_slots(self):
        self.c_VNavigationBar.currentItemChanged.connect(self.stackedWidget.setCurrentIndex)

    def set_navigationBar(self):
        self.c_VNavigationBar = QVNavigationBar()
        self.stackedWidget = QStackedWidget(self)

        self.c_VNavigationBar.addItem("发现音乐")
        self.c_VNavigationBar.addItem("私人FM")
        self.c_VNavigationBar.addItem("MV")
        self.c_VNavigationBar.addItem("朋友")
        self.c_VNavigationBar.addItem("本地音乐")
        self.c_VNavigationBar.addItem("下载管理")
        self.c_VNavigationBar.addItem("我的音乐云盘")
        self.c_VNavigationBar.addItem("我的收藏")

        self.c_ui_locallist = ui_locallist(self)
        self.c_ui_searchedlist = ui_searchedlist(self)
        self.stackedWidget.addWidget(self.c_ui_searchedlist)
        self.stackedWidget.addWidget(QLabel("开发中,敬请期待"))
        self.stackedWidget.addWidget(QLabel("开发中,敬请期待"))
        self.stackedWidget.addWidget(QLabel("开发中,敬请期待"))
        self.stackedWidget.addWidget(self.c_ui_locallist)
        self.stackedWidget.addWidget(QLabel("开发中,敬请期待"))
        self.stackedWidget.addWidget(QLabel("开发中,敬请期待"))
        self.stackedWidget.addWidget(QLabel("开发中,敬请期待"))

    def set_layout(self):
        self.c_ui_player = ui_palyer(self)
        self.c_ui_playlist = ui_playlist(self)

        # 布局
        layout_1 = QVBoxLayout()
        layout_2 = QHBoxLayout()

        layout_1.setContentsMargins(0, 0, 0, 0)
        layout_1.setSpacing(0)
        layout_2.setContentsMargins(0, 0, 0, 0)
        layout_2.setSpacing(0)

        layout_1.addLayout(layout_2)
        layout_1.addWidget(self.c_ui_player)

        layout_2.addWidget(self.c_VNavigationBar)
        layout_2.addWidget(self.stackedWidget)
        layout_2.addWidget(self.c_ui_playlist)

        self.widget_central = QWidget()
        self.widget_central.setLayout(layout_1)
        self.setCentralWidget(self.widget_central)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ui_mainwindow()
    w.show()
    sys.exit(app.exec_())



