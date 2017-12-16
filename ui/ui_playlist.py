# -*- coding: utf-8 -*-
import os
import sys
import os.path
os.chdir(os.path.split(os.path.realpath(__file__))[0])
sys.path.append("../res")
sys.path.append("../ui")
sys.path.append("../qss")

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *

import time

class ui_playlist(QListView):

    # signal_playlist_add = pyqtSignal()
    # signal_playlist_clear = pyqtSignal()
    # signal_playlist_set_row = pyqtSignal()

    def __init__(self, parent=None):
        super(ui_playlist, self).__init__()
        self.p_main = parent

        self.setupUi()
        self.connect_signals_slots()

        self.update_playlist()

        self.currentrow = -1

    def setupUi(self):
        # 绑定模型/视图
        self.list_playlist = []
        self.model_playlist = QStringListModel()

        self.model_playlist.setStringList(self.list_playlist)
        self.setModel(self.model_playlist)

        self.setUpdatesEnabled(True)

        # 添加Action
        self.set_action()
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addAction(self.action_add)
        self.addAction(self.action_del)
        self.addAction(self.action_clear)

        # 外观设计
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFixedWidth(200)

        
        with open("../qss/ui_playlist.qss", "r") as file:
            self.setStyleSheet(file.read())

    def connect_signals_slots(self):
        self.action_add.triggered.connect(self.on_playerlist_add)
        self.action_del.triggered.connect(self.on_playerlist_del)
        self.action_clear.triggered.connect(self.on_playerlist_clear)
        self.doubleClicked.connect(self.on_playerlist_dbclick)


    def set_action(self):
        self.action_add = QAction("&Add", self)
        self.action_del = QAction("Del", self)
        self.action_clear = QAction("&Clear", self)


    def update_playlist(self):
        self.list_playlist.clear()
        for line in open("../res/playlist.m3u"):
            line_split_name = line.split("/")[-1].split(".")[0]
            self.list_playlist.append(line_split_name)
        self.model_playlist.setStringList(self.list_playlist)

    def on_playerlist_add(self):
        self.p_main.c_ui_player.playlist_add()
        self.update_playlist()

    def on_playerlist_del(self):
        row = self.currentIndex().row()
        self.p_main.c_ui_player.playlist_del(row)
        self.update_playlist()

    def on_playerlist_clear(self):
        self.p_main.c_ui_player.playlist_clear()
        self.update_playlist()

    def on_playerlist_dbclick(self):
        row = self.currentIndex().row()
        # 如果双击项是当前播放项,那么暂停/播放. 否则,选中并开始播放
        if self.currentrow == row:   
            if self.p_main.c_ui_player.player.state() == QMediaPlayer.PlayingState:
                self.p_main.c_ui_player.player.pause()
            else:
                self.p_main.c_ui_player.player.play()
        else:
            self.p_main.c_ui_player.playlist_set_index(row)
            self.currentrow = row

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ui_playlist()
    w.show()
    sys.exit(app.exec_())