import sqlite3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from interface_ind import Ui_MainWindow as interfaceUI
from clients import Ui_Dialog as clientsUI
from orders import Ui_Dialog as ordersUI
from medicine import Ui_Dialog as medicineUI

class main_window(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = interfaceUI()
        self.ui.setupUi(self)

        self.ui.comboBox.currentTextChanged.connect(self.load_table)
        self.ui.pushButton.clicked.connect(self.open_add_form)
        self.ui.tableWidget.itemClicked.connect(self.open_update_form)

        self.load_tables()
        self.read_clients()

    def load_tables(self):
        cursor.execute('SELECT name FROM sqlite_master WHERE type = "table"')
        tables = cursor.fetchall()
        print(tables)
        for table in tables:
            self.ui.comboBox.addItem(table[0])

    def load_table(self):
        print(self.ui.comboBox.currentText())
        if self.ui.comboBox.currentText() == 'Препараты':
            self.read_medicine()
        elif self.ui.comboBox.currentText() == 'Оптовые_клиенты':
            self.read_clients()
        else:
            self.read_orders()

    def read_medicine(self):
        print()
        self.ui.tableWidget.setRowCount(0)
        cursor.execute('SELECT * FROM "Препараты"')
        self.medicine_data = cursor.fetchall()

        self.ui.tableWidget.setColumnCount(3)
        self.ui.tableWidget.setHorizontalHeaderLabels(['Препараты', 'Цена'])

        self.ui.tableWidget.setRowCount(len(self.medicine_data))
        for row in range(len(self.medicine_data)):
            text = (str(self.medicine_data[row][0]) + ' | ' + str(self.medicine_data[row][1])
                    + '\n' + str(self.medicine_data[row][2])
                    + '\nУпаковка: ' + str(self.medicine_data[row][3]) + '\nСертификат: '
                    + str(self.medicine_data[row][5]))
            item = QTableWidgetItem()
            item.setText(text)
            self.ui.tableWidget.setItem(row, 0, item)
            price = str(self.medicine_data[row][4])
            item = QTableWidgetItem()
            item.setText(price)
            self.ui.tableWidget.setItem(row, 1, item)
            item = QTableWidgetItem()
            icon_path = 'filler2.png'
            icon = QIcon(icon_path)
            item.setIcon(icon)
            self.ui.tableWidget.setItem(row, 2, item)
            self.ui.tableWidget.setIconSize(QSize(70, 70))

        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.resizeRowsToContents()

    def read_clients(self):
        print()
        self.ui.tableWidget.setRowCount(0)
        cursor.execute('SELECT * FROM Оптовые_клиенты')
        self.client_data = cursor.fetchall()

        self.ui.tableWidget.setColumnCount(2)
        self.ui.tableWidget.setHorizontalHeaderLabels(['Клиенты', 'Изображение'])

        self.ui.tableWidget.setRowCount(len(self.client_data))
        for row in range(len(self.client_data)):
            text = (str(self.client_data[row][0]) + ' | ' + str(self.client_data[row][1])
                    + '\n' + str(self.client_data[row][2])
                    + '\n' + str(self.client_data[row][3]) + '\nГород: '
                    + str(self.client_data[row][4]))
            item = QTableWidgetItem()
            item.setText(text)
            self.ui.tableWidget.setItem(row, 0, item)
            item = QTableWidgetItem()
            icon_path = 'filler2.png'
            icon = QIcon(icon_path)
            item.setIcon(icon)
            self.ui.tableWidget.setItem(row, 1, item)
            self.ui.tableWidget.setIconSize(QSize(70, 70))


        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.resizeRowsToContents()

    def read_orders(self):
        print()
        self.ui.tableWidget.setRowCount(0)
        cursor.execute('SELECT * FROM Заказы')
        self.medicine_data = cursor.fetchall()

        self.ui.tableWidget.setColumnCount(3)
        self.ui.tableWidget.setHorizontalHeaderLabels(['Заказы', 'Скидка'])

        self.ui.tableWidget.setRowCount(len(self.medicine_data))
        for row in range(len(self.medicine_data)):
            text = (str(self.medicine_data[row][0]) + ' | ' + str(self.medicine_data[row][1])
                    + ' | ' + str(self.medicine_data[row][2])
                    + '\n' + str(self.medicine_data[row][3]) + '\nКоличество: '
                    + str(self.medicine_data[row][4]))
            item = QTableWidgetItem()
            item.setText(text)
            self.ui.tableWidget.setItem(row, 0, item)
            price = str(self.medicine_data[row][5])
            item = QTableWidgetItem()
            item.setText(price)
            self.ui.tableWidget.setItem(row, 1, item)

        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.resizeRowsToContents()

    def open_add_form(self):
        self.client_form = client_window(self)
        self.client_form.ui.pushButton.clicked.connect(self.client_form.create_client)
        self.client_form.exec()

    def open_update_form(self):
        self.client_form = client_window(self)
        client_data = self.client_data[self.ui.tableWidget.currentRow()]
        self.client_form.inn = client_data[0]

        self.client_form.ui.lineEdit.setText(str(client_data[0]))
        self.client_form.ui.lineEdit_2.setText(str(client_data[1]))
        self.client_form.ui.lineEdit_3.setText(str(client_data[2]))
        self.client_form.ui.lineEdit_4.setText(str(client_data[3]))
        self.client_form.ui.lineEdit_5.setText(str(client_data[4]))

        self.client_form.ui.pushButton.clicked.connect(self.client_form.update_client)
        self.client_form.exec()

class client_window(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = clientsUI()
        self.ui.setupUi(self)

    def create_client(self):
        client_data = [
                       self.ui.lineEdit_2.text(),
                       self.ui.lineEdit_3.text(),
                       self.ui.lineEdit_4.text(),
                       self.ui.lineEdit_5.text()]
        if any([item == '' for item in client_data]):
            QMessageBox.critical(self, 'Not done', 'Fill all fields', QMessageBox.Ok)
            return
        q = QMessageBox.critical(self, 'Commit action', 'Do you really want to add a client?',
                                 QMessageBox.Ok|QMessageBox.Cancel)
        if q == QMessageBox.Ok:
            try:
                cursor.execute('INSERT INTO Оптовые_клиенты VALUES(NULL,?,?,?,?)', client_data)
                conn.commit()
                main_form.read_clients()
                return
            except:
                QMessageBox.critical(self, 'Error', 'Adding error', QMessageBox.Ok)

    def update_client(self):
        client_id = self.inn
        client_data = [
                       self.ui.lineEdit_2.text(),
                       self.ui.lineEdit_3.text(),
                       self.ui.lineEdit_4.text(),
                       self.ui.lineEdit_5.text()]
        if any([item == '' for item in client_data]):
            QMessageBox.critical(self, 'Not done', 'Fill all fields', QMessageBox.Ok)
            return
        q = QMessageBox.critical(self, 'Commit action', 'Do you really want to change a client?',
                                 QMessageBox.Ok|QMessageBox.Cancel)
        if q == QMessageBox.Ok:
            try:
                cursor.execute(f'UPDATE Оптовые_клиенты SET surname = ?, name = ?, patronymic = ?, city = ? WHERE client_number = {client_id}', client_data)
                conn.commit()
                main_form.read_clients()
                return
            except:
                QMessageBox.critical(self, 'Error', 'Adding error', QMessageBox.Ok)
    
        

if __name__ == "__main__":
    app = QApplication(sys.argv)  
    conn = sqlite3.connect('Микстура.db')  
    cursor = conn.cursor()
    main_form = main_window()  
    main_form.show()  
    sys.exit(app.exec_())  
    cursor.close()  
    conn.close()
