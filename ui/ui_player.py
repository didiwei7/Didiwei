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
class ui_palyer(QFrame):

    def __init__(self, parent=None):
        super(ui_palyer, self).__init__()
        self.p_main = parent

        # int
        self.flag_volume = 0
        self.value_volume = 0

        self.setupUi()
        self.init_player()
        self.connect_signals_slots()

    def setupUi(self):
        self.set_btn()
        self.set_label()
        self.set_slider()
        self.set_layout()

        self.setFixedHeight(50)
        self.setMouseTracking(True)

        with open("../qss/ui_player.qss", "r") as file:
            self.setStyleSheet(file.read())

    def init_player(self):
        self.playlist = QMediaPlaylist()
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        # self.playlist_load()
        
        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)

    def connect_signals_slots(self):
        self.btn_play_pause.clicked.connect(self.on_play_pause)
        self.btn_pre.clicked.connect(self.playlist.previous)
        self.btn_next.clicked.connect(self.playlist.next)

        self.slider_sound.valueChanged.connect(self.player.setVolume)
        self.btn_sound.clicked.connect(self.on_volume)
        self.btn_loop.clicked.connect(self.on_loop)
        self.btn_playlist.clicked.connect(self.on_playlist)

        self.player.durationChanged.connect(self.update_duration)
        self.player.positionChanged.connect(self.update_position)
        self.slider_duration.valueChanged.connect(self.update_position_set)
        self.player.stateChanged.connect(self.update_status)


    def set_label(self):
        # 歌曲进度更新
        self.label_duration_now = QLabel()
        self.label_duration_all = QLabel()

        self.label_duration_now.setText("00.00")
        self.label_duration_all.setText("00.00")

    def set_btn(self):
        # 播放
        self.btn_pre = QToolButton()
        self.btn_next = QToolButton()
        self.btn_play_pause = QToolButton()

        # 音量
        self.btn_sound = QToolButton()

        # 循环
        self.btn_loop = QToolButton()
        
        # 播放列表 显示/隐藏
        self.btn_playlist = QToolButton()

        self.btn_pre.setIcon(QIcon("../res/music_pre.png"))
        self.btn_play_pause.setIcon(QIcon("../res/music_play.png"))
        self.btn_next.setIcon(QIcon("../res/music_next"))

        self.btn_sound.setIcon(QIcon("../res/music_sound.png"))
        self.btn_loop.setIcon(QIcon("../res/music_loop_list.png"))
        self.btn_playlist.setIcon(QIcon("../res/music_playlist.png"))

    def set_slider(self):
        # 歌曲进度
        self.slider_duration = QSlider(Qt.Horizontal)
        self.slider_duration.setMinimumWidth(300)
        self.slider_duration.setObjectName("slider_duration")

        # 音量
        self.slider_sound = QSlider(Qt.Horizontal)
        self.slider_sound.setFixedWidth(100)
        self.slider_sound.setValue(50)

    def set_layout(self):
        # 布局
        layout_1 = QHBoxLayout()
        layout_1.addSpacing(20)
        layout_1.addWidget(self.btn_pre)
        layout_1.addWidget(self.btn_play_pause)
        layout_1.addWidget(self.btn_next)
        layout_1.addSpacing(20)

        layout_1.addWidget(self.label_duration_now)
        layout_1.addWidget(self.slider_duration)
        layout_1.addWidget(self.label_duration_all)

        layout_1.addWidget(self.btn_sound)
        layout_1.addWidget(self.slider_sound)

        layout_1.addWidget(self.btn_loop)
        layout_1.addWidget(self.btn_playlist)

        self.setLayout(layout_1)


    def on_volume(self):
        if 0 == self.flag_volume:
            self.flag_volume = 1
            self.value_volume = self.slider_sound.value()
            self.slider_sound.setValue(0)
            self.btn_sound.setIcon(QIcon("../res/music_sound_off.png"))
            self.slider_sound.setEnabled(False)
        else:
            self.slider_sound.setEnabled(True)
            self.slider_sound.setValue(self.value_volume)
            self.btn_sound.setIcon(QIcon("../res/music_sound.png"))
            self.flag_volume = 0

    def on_loop(self):
        if self.playlist.playbackMode() == QMediaPlaylist.Loop:
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
            self.btn_loop.setIcon(QIcon("../res/music_loop_single.png"))
        elif self.playlist.playbackMode() == QMediaPlaylist.CurrentItemInLoop:
            self.playlist.setPlaybackMode(QMediaPlaylist.Random)
            self.btn_loop.setIcon(QIcon("../res/music_loop_random.png"))
        elif self.playlist.playbackMode() == QMediaPlaylist.Random:
            self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
            self.btn_loop.setIcon(QIcon("../res/music_loop_list.png"))

    def on_play_pause(self):
        if self.player.mediaStatus() == QMediaPlayer.NoMedia:
            self.playlist_add()
        elif self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.btn_play_pause.setIcon(QIcon("../res/music_play.png"))
        else:
            self.player.play()
            self.btn_play_pause.setIcon(QIcon("../res/music_pause.png"))

    def on_playlist(self):
        if self.p_main.c_ui_playlist.isVisible():
            self.p_main.c_ui_playlist.hide()
        else:
            self.p_main.c_ui_playlist.show()


    def playlist_load(self):
        file = QFile("../res/playlist.m3u")
        file.open(QIODevice.ReadOnly)
        self.playlist.load(file, "m3u")
        file.close()

    def playlist_save(self):
        file = QFile("../res/playlist.m3u")
        file.open(QIODevice.WriteOnly)
        self.playlist.save(file, "m3u")
        file.close()

    def playlist_add(self):
        musicPath = QStandardPaths.standardLocations(QStandardPaths.MusicLocation)
        filePath, _ = QFileDialog.getOpenFileName(self, "Open File", musicPath[0], "mp3(*.mp3)")
        if filePath.strip() == "":
            return
        else:
            # 如果playlist为空,需要从新载入. 
            if self.playlist.isEmpty():
               self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(filePath)))
               self.player.setPlaylist(self.playlist)
               self.playlist_save()
               # 小Bug,解决,通过按钮"播放"打开文件后, 播放列表不更新
               self.p_main.c_ui_playlist.update_playlist()
            else:
                self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(filePath)))
                self.playlist_save()

    def playlist_clear(self):
        self.player.stop()
        self.playlist.clear()
        time.sleep(0.01)
        self.playlist_save()

    def playlist_del(self, index):
        self.playlist.removeMedia(index)
        self.playlist_save()

    def playlist_set_index(self, index):
        self.player.stop()
        self.playlist.setCurrentIndex(index)
        self.player.play()


    def update_status(self, state):
        if state == QMediaPlayer.PlayingState:
            self.btn_play_pause.setIcon(QIcon("../res/music_pause.png"))
        else:
            self.btn_play_pause.setIcon(QIcon("../res/music_play.png"))

    def update_duration(self, duration):
        self.slider_duration.setRange(0, duration)
        self.slider_duration.setEnabled(True)
        self.slider_duration.setPageStep(int(duration / 10))

        # 更新 Label 歌曲总时间
        m_duration = QTime(0, duration / 60000, qRound((duration % 60000) / 1000.0))
        self.label_duration_all.setText(m_duration.toString("mm:ss"))

    def update_position(self, position):
        self.slider_duration.setValue(position)
        m_duration = QTime(0, position / 60000, qRound((position % 60000) / 1000.0))
        self.label_duration_now.setText(m_duration.toString("mm:ss"))

    def update_position_set(self, position):
        if qAbs(self.player.position() - position) > 99:
            self.player.setPosition(position)

    def closeEvent(self, event):
        self.playlist_save()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ui_palyer()
    w.show()
    sys.exit(app.exec_())