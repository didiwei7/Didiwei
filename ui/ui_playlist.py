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
from PyQt5.QtSql import *
from PyQt5.QtMultimedia import *

import time

class ui_playlist(QFrame):

    def __init__(self, parent=None):
        super(ui_playlist, self).__init__()
        self.p_main = parent

        self.connect_to_datebase()
        self.setupUi()
        self.connect_signals_slots()
        self.currentrow = -1

    def setupUi(self):
        self.connect_to_datebase()
        self.set_action()
        self.set_tableView()
        self.set_layout()

        # 外观设计
        self.setFixedWidth(300)
        with open("../qss/ui_playlist.qss", "r") as file:
            self.setStyleSheet(file.read())

    def connect_signals_slots(self):
        self.action_add.triggered.connect(self.on_playerlist_add)
        self.action_del.triggered.connect(self.on_playerlist_del)
        self.action_clear.triggered.connect(self.on_playerlist_clear)
        self.tableView.doubleClicked.connect(self.on_playerlist_dbclick)


    def set_action(self):
        self.action_add = QAction("&Add", self)
        self.action_del = QAction("Del", self)
        self.action_clear = QAction("&Clear", self)

    def set_tableView(self):
        self.model = QSqlTableModel()
        # 设置提交方式
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        # 选中表
        self.model.setTable("playlist")
        # 更改表头信息
        self.model.setHeaderData(self.model.fieldIndex("name"), Qt.Horizontal, "音乐")
        self.model.setHeaderData(self.model.fieldIndex("author"), Qt.Horizontal, "歌手")
        # 排序 从0行升序
        self.model.setSort(0, Qt.AscendingOrder)
        # 选中绑定内容
        self.model.select()

        self.tableView = QTableView()
        self.tableView.setModel(self.model)
        # 隐藏行
        self.tableView.setColumnHidden(self.model.fieldIndex("id"), True)
        self.tableView.setColumnHidden(self.model.fieldIndex("type"), True)
        self.tableView.setColumnHidden(self.model.fieldIndex("musicid"), True)
        self.tableView.setColumnHidden(self.model.fieldIndex("filepath"), True)
        # 表格样式 网格背景虚线
        self.tableView.setShowGrid(True)
        self.tableView.setGridStyle(Qt.DotLine)
        # 开启右键点击事件
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        # 整行选中
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers); 
        # 排序
        self.tableView.setSortingEnabled(False)

        self.tableView.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.tableView.addAction(self.action_add)
        self.tableView.addAction(self.action_del)
        self.tableView.addAction(self.action_clear)

    def set_layout(self):
        layout_1 = QVBoxLayout()
        layout_1.setContentsMargins(0, 0, 0, 0)
        layout_1.setSpacing(0)

        layout_1.addWidget(self.tableView)
        self.setLayout(layout_1)

    # def update_playlist(self):
    #     self.list_playlist.clear()
    #     for line in open("../res/playlist.m3u"):
    #         line_split_name = line.split("/")[-1].split(".")[0]
    #         self.list_playlist.append(line_split_name)
    #     self.model_playlist.setStringList(self.list_playlist)

    def on_playerlist_add(self):
        musicPath = QStandardPaths.standardLocations(QStandardPaths.MusicLocation)
        filePath, _ = QFileDialog.getOpenFileName(self, "Open File", musicPath[0], "mp3(*.mp3)")
        if filePath.strip() == "":
            return
        else:
            name_tmp = filePath.split("/")[-1].split(".")[0].split(" - ")[-1]
            author_tmp = filePath.split("/")[-1].split(".")[0].split(" - ")[0]
            type_tmp = 0
            musicid_tmp = ""
            filepath_tmp = filePath

            row_count = self.model.rowCount()
            record = self.model.record()
            record.setValue("id", row_count)
            record.setValue("name", name_tmp)
            record.setValue("author", author_tmp)
            record.setValue("type", type_tmp)
            record.setValue("musicid", musicid_tmp)
            record.setValue("filepath", filepath_tmp)
            self.model.insertRecord(row_count, record)
            self.model.submitAll()

    def on_playerlist_del(self):
        row = self.tableView.currentIndex().row()
        row_count = self.model.rowCount()
        self.model.removeRow(row)
        self.model.submitAll();
        for i in range(row, row_count-1, 1):
            self.model.setData(self.model.index(i, 0), i)
            self.model.submitAll();

    def on_playerlist_clear(self):
        row_count = self.model.rowCount()
        self.model.removeRows(0, rowcount)
        self.model.submitAll()

    def on_playerlist_dbclick(self):
        row = self.tableView.currentIndex().row()
        # 如果双击项是当前播放项,那么暂停/播放. 否则,选中并开始播放
        if self.currentrow == row:   
            if self.p_main.c_ui_player.player.state() == QMediaPlayer.PlayingState:
                self.p_main.c_ui_player.player.pause()
            else:
                self.p_main.c_ui_player.player.play()
        else:
            str_filepath = str(self.model.record(row).value("filepath"))
            self.p_main.c_ui_player.player.setMedia(QMediaContent(QUrl.fromLocalFile(str_filepath)))
            self.p_main.c_ui_player.player.play()
            self.currentrow = row


    def connect_to_datebase(self):
        filename = "../db/db_playlist.db"
        flag_creat = QFile.exists(filename)

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("../db/db_playlist.db")

        if not db.open():
            print (db.lastError().text())

        if not flag_creat:
            query = QSqlQuery()
            query.exec_("create table playlist(id integer primary key, name varchar, author varchar, type integer, musicid varchar, filepath varchar)")
        else:
            print ("连接数据库成功")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ui_playlist()
    w.show()
    sys.exit(app.exec_())