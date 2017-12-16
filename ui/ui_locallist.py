# -*- coding: utf-8 -*-
import os
import sys
import os.path
os.chdir(os.path.split(os.path.realpath(__file__))[0])
sys.path.append("../res")
sys.path.append("../ui")
sys.path.append("../qss")
sys.path.append("../db")

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtMultimedia import *

import time

class ui_locallist(QWidget):

    def __init__(self, parent=None):
        super(ui_locallist, self).__init__()
        self.p_main = parent

        self.connect_to_datebase()
        self.setupUi()

    def setupUi(self):
        self.set_btn()
        self.set_label()
        self.set_tableView()
        self.set_layout()

        with open("../qss/ui_locallist.qss", "r") as file:
            self.setStyleSheet(file.read())


    def connect_signals_slots(self):
        pass

    def set_label(self):
        self.lable_1 = QLabel("本地音乐")

    def set_btn(self):
        self.btn_openfile = QPushButton("选择目录")

    def set_tableView(self):
        self.modle = QSqlTableModel()
        # 设置提交方式
        self.modle.setEditStrategy(QSqlTableModel.OnManualSubmit)
        # 选中表
        self.modle.setTable("local")
        # 更改表头信息
        self.modle.setHeaderData(self.modle.fieldIndex("name"), Qt.Horizontal, "音乐")
        self.modle.setHeaderData(self.modle.fieldIndex("author"), Qt.Horizontal, "歌手")
        # 排序 从0行升序
        self.modle.setSort(0, Qt.AscendingOrder)
        # 选中绑定内容
        self.modle.select()

        self.tableView = QTableView()
        self.tableView.setModel(self.modle)
        # 隐藏行
        # self.tableView.setColumnHidden(self.modle.fieldIndex("id"), True)
        # 表格样式 网格背景虚线
        self.tableView.setShowGrid(True)
        self.tableView.setGridStyle(Qt.DotLine)
        # 开启右键点击事件
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        # 整行选中
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 排序
        self.tableView.setSortingEnabled(False)

    def set_layout(self):
        layout_1 = QVBoxLayout()
        layout_2 = QHBoxLayout()

        layout_1.setContentsMargins(0, 0, 0, 0)
        layout_1.setSpacing(0)
        layout_2.setContentsMargins(0, 0, 0, 0)
        layout_2.setSpacing(0)

        layout_1.addLayout(layout_2)
        layout_1.addWidget(self.tableView)

        layout_2.addWidget(self.lable_1)
        layout_2.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout_2.addWidget(self.btn_openfile)
        

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
            query.exec_("create table lacal(id integer primary key, name varchar, author varchar, filepath varchar)")
        else:
            print ("连接数据库成功")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ui_locallist()
    w.show()
    sys.exit(app.exec_())