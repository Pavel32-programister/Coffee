import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        res = cur.execute("select * from Coffee").fetchall()
        self.Table.setRowCount(len(res))
        for i in range(len(res)):
            self.Table.setItem(i, 0, QTableWidgetItem(str(res[i][1])))
            self.Table.setItem(i, 1, QTableWidgetItem(str(res[i][2])))
            self.Table.setItem(i, 2, QTableWidgetItem(str(res[i][3])))
            self.Table.setItem(i, 3, QTableWidgetItem(str(res[i][4])))
        con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())