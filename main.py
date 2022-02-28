import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget

from UI.addEditCoffeeForm import Ui_Form
from UI.main import Ui_MainWindow


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.form = AddEdit(self)

        self.Table.clicked.connect(self.editCoffee)
        self.AddCoffee.clicked.connect(self.addCoffee)
        self.upd()

    def upd(self):
        con = sqlite3.connect("data/coffee.sqlite")
        cur = con.cursor()
        res = cur.execute("select * from Coffee").fetchall()
        self.Table.setRowCount(len(res))
        for i in range(len(res)):
            self.Table.setItem(i, 0, QTableWidgetItem(str(res[i][0])))
            self.Table.setItem(i, 1, QTableWidgetItem(str(res[i][1])))
            self.Table.setItem(i, 2, QTableWidgetItem(str(res[i][2])))
            self.Table.setItem(i, 3, QTableWidgetItem(str(res[i][3])))
            self.Table.setItem(i, 4, QTableWidgetItem(str(res[i][4])))
        con.close()

    def addCoffee(self):
        self.form.add()
        self.form.show()

    def editCoffee(self):
        r = [i.row() for i in self.Table.selectedItems()][0]
        id = self.Table.item(r, 0).text()
        name = self.Table.item(r, 1).text()
        surname = self.Table.item(r, 2).text()
        value = self.Table.item(r, 3).text()
        price = self.Table.item(r, 4).text()
        self.form.edit(id, name, surname, value, price)
        self.form.show()


class AddEdit(QWidget, Ui_Form):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parr = parent
        self.Yes.clicked.connect(self.confirm)
        self.No.clicked.connect(self.close)
        self.type = ""
        self.id = ""

    def add(self):
        self.Name.setText("")
        self.SortName.setText("")
        self.Value.setValue(0)
        self.Price.setValue(0)
        self.type = "add"

    def edit(self, id, name, surname, value, price):
        self.type = "edit"
        self.id = id
        self.Name.setText(name)
        self.SortName.setText(surname)
        self.Value.setValue(int(value))
        self.Price.setValue(int(price))

    def confirm(self):
        con = sqlite3.connect("data/coffee.sqlite")
        cur = con.cursor()
        if self.type == "add":
            name = self.Name.text()
            surname = self.SortName.text()
            value = self.Value.value()
            price = self.Price.value()
            cur.execute(f"insert into Coffee(name, seedSort, value, price)"
                        f" values('{name}', '{surname}', {value}, {price})")
            con.commit()
            self.parr.upd()
        elif self.type == "edit":
            id = self.id
            name = self.Name.text()
            surname = self.SortName.text()
            value = self.Value.value()
            price = self.Price.value()
            cur.execute(f"Update Coffee "
                        f"Set name = '{name}', seedSort = '{surname}', "
                        f"value = {value}, price = {price} "
                        f"where id = {self.id}")
            con.commit()
            self.parr.upd()
        con.close()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())