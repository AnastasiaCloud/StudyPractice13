import sqlite3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
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

        self.load_tables()
        self.read_medicine()

    def load_tables(self):
        cursor.execute('SELECT name FROM sqlite_master WHERE type = "table"')
        tables = cursor.fetchall()
        for table in tables:
            self.ui.comboBox.addItem(table[0])

    def load_table(self):
        if self.ui.comboBox.currentText() == 'Препараты':
            self.read_medicine()
        elif self.ui.comboBox.currentText() == 'Оптовые_клиенты':
            self.read_clients()
        else:
            self.read_orders()

    def read_medicine(self):
        self.ui.tableWidget.setRowCount(0)
        cursor.execute('SELECT * FROM Препараты')
        self.medicine_data = cursor.fetchall()

        self.ui.tableWidget.setColumnCount(2)
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

        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.resizeRowsToContents()

    def read_clients():
        print()

    def read_orders():
        print()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)  
    conn = sqlite3.connect('Микстура.db')  
    cursor = conn.cursor()
    main_form = main_window()  
    main_form.show()  
    sys.exit(app.exec_())  
    cursor.close()  
    conn.close()
