import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


import sys
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import *


def creatDB():
    db = QSqlDatabase.addDatabase("QSQLITE")
    # 指定SQLite数据库的文件名
    db.setDatabaseName("AlloySupermarket/res/AsDB.db")
    if not db.open():
        print("无法建立与数据库的连接")
    query = QSqlQuery()
    # qurey.exec('create table people(id int primary key,name varchar(10),address varchar(50))')
    # qurey.exec('insert into people values(1,"李宁","Shenyang")')
    # qurey.exec('SELECT UTS FROM Al_Si-Mg-Sc')
    query.prepare('select Al, Si, Mg, Sc, UTS, YS, EL from Al_Si_Mg_Sc')
    if not query.exec_():
        query.lastError()
    else:
        while query.next():
            Al = query.value(0)
            Si = query.value(1)
            Mg = query.value(2)
            Sc = query.value(3)
            UTS = query.value(4)
            YS = query.value(5)
            EL = query.value(6)
            print(Al, Si, Mg, Sc, UTS, YS, EL)

    db.close()


if __name__ == "__main__":
    creatDB()
