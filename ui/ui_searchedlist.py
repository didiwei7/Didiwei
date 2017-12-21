# -*- coding: utf-8 -*-
import os
import sys
import os.path
import json
os.chdir(os.path.split(os.path.realpath(__file__))[0])
sys.path.append("../res")
sys.path.append("../ui")
sys.path.append("../qss")
sys.path.append("../db")
sys.path.append("../api")

from netease import *
from myapi import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtMultimedia import *

import time

class ui_searchedlist(QWidget):

    def __init__(self, parent=None):
        super(ui_searchedlist, self).__init__()
        self.p_main = parent

        # self.connect_to_datebase()
        self.setupUi()
        self.connect_signals_slots()

    def setupUi(self):
        self.set_btn()
        self.set_label()
        self.set_edit()
        self.set_tableView()
        self.set_layout()

    def connect_signals_slots(self):
        self.btn_search.clicked.connect(self.on_search)
        self.tableView.doubleClicked.connect(self.on_double_clicked_play)

    def set_edit(self):
        self.edit_search = QLineEdit()
        self.edit_search.setFixedWidth(100)

    def set_label(self):
        pass

    def set_btn(self):
        self.btn_search = QPushButton("搜索")

    def set_tableView(self):
        self.model = QSqlTableModel()
        # 设置提交方式
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        # 选中表
        self.model.setTable("searched")
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
        # self.tableView.setColumnHidden(self.model.fieldIndex("id"), True)
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

    def set_layout(self):
        layout_1 = QVBoxLayout()
        layout_2 = QHBoxLayout()

        layout_1.setContentsMargins(0, 0, 0, 0)
        layout_1.setSpacing(0)
        layout_2.setContentsMargins(5, 5, 5, 5)
        layout_2.setSpacing(5)

        layout_1.addLayout(layout_2)
        layout_1.addWidget(self.tableView)

        layout_2.addWidget(self.edit_search)
        layout_2.addWidget(self.btn_search)
        layout_2.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.setLayout(layout_1)

    def connect_to_datebase(self):
        filename = "../db/db_playlist.db"
        flag_creat = QFile.exists(filename)

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("../db/db_playlist.db")

        if not db.open():
            print (db.lastError().text())

        if not flag_creat:
            query = QSqlQuery()
            query.exec_("create table searched(id integer primary key, name varchar, author varchar, musicid varchar, filepath varchar)")
        else:
            print ("连接数据库成功")

    def on_search(self):
        rowcount = self.model.rowCount()
        self.model.removeRows(0, rowcount)
        self.model.submitAll()
        myapi = myApi()
        searchedList = myapi.get_songnames_songids_by_artistid(self.edit_search.text())
        for i in range(0, 50):
            row = self.model.rowCount()
            record = QSqlRecord()
            record = self.model.record()
            record.setValue('id', row)
            record.setValue('name', searchedList['Num{0}'.format(i)]['name'])
            record.setValue('author', " ")
            record.setValue('musicid', searchedList['Num{0}'.format(i)]['id'])
            record.setValue('filepath', " ")
            self.model.insertRecord(0, record)
            self.model.submitAll()

    def on_double_clicked_play(self):
        # 获取当前选中行数据
        row  = self.tableView.currentIndex().row()
        name_tmp  = self.model.record(row).value("name")
        author_tmp = ""
        type_tmp = 1
        musicid_tmp = self.model.record(row).value("musicid")
        filepath_tmp = ""
        # 添加到播放列表
        row_count = self.p_main.c_ui_playlist.model.rowCount()
        record = self.p_main.c_ui_playlist.model.record()
        record.setValue("id", row_count)
        record.setValue("name", name_tmp)
        record.setValue("author", author_tmp)
        record.setValue("type", type_tmp)
        record.setValue("musicid", musicid_tmp)
        record.setValue("filepath", filepath_tmp)
        self.p_main.c_ui_playlist.model.insertRecord(row_count, record)
        self.p_main.c_ui_playlist.model.submitAll()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ui_searchedlist()
    w.show()
    sys.exit(app.exec_())