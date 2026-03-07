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

from login import Ui_MainWindow as LoginUI

LOGIN = "admin"
PASSWORD = "admin"

class LoginWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = LoginUI()
        self.ui.setupUi(self)

        #Подключаем кнопку
        self.ui.pushButton.clicked.connect(self.login)
        self.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
    #В фукнкции проверяем совпадают ли введеные данные с заданными
    def login(self):
        if self.ui.lineEdit.text() == LOGIN and self.ui.lineEdit_2.text() == PASSWORD:
            self.main_form = main_window()  
            self.main_form.show()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

            
class main_window(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = interfaceUI()
        self.ui.setupUi(self)

        self.ui.comboBox.currentTextChanged.connect(self.load_table)
        self.ui.pushButton.clicked.connect(self.open_add_form)
        self.ui.pushButton_2.clicked.connect(self.delete_row)
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
            self.ui.tableWidget.setIconSize(QSize(100, 100))

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
            self.ui.tableWidget.setIconSize(QSize(100, 100))


        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.resizeRowsToContents()

    def read_orders(self):
        print()
        self.ui.tableWidget.setRowCount(0)
        cursor.execute('SELECT * FROM Заказы')
        self.orders_data = cursor.fetchall()

        self.ui.tableWidget.setColumnCount(2)
        self.ui.tableWidget.setHorizontalHeaderLabels(['Заказы', 'Скидка'])

        self.ui.tableWidget.setRowCount(len(self.orders_data))
        for row in range(len(self.orders_data)):
            text = (str(self.orders_data[row][0]) + ' | ' + str(self.orders_data[row][1])
                    + ' | ' + str(self.orders_data[row][2])
                    + '\n' + str(self.orders_data[row][3]) + '\nКоличество: '
                    + str(self.orders_data[row][4]))
            item = QTableWidgetItem()
            item.setText(text)
            self.ui.tableWidget.setItem(row, 0, item)
            price = str(self.orders_data[row][5])
            item = QTableWidgetItem()
            item.setText(price)
            self.ui.tableWidget.setItem(row, 1, item)

        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.resizeRowsToContents()

    def open_add_form(self):
        current_table = self.ui.comboBox.currentText()
        
        if current_table == 'Оптовые_клиенты':
            self.client_form = client_window(self)
            self.client_form.ui.pushButton.clicked.connect(self.client_form.create_client)
            self.client_form.exec()
        elif current_table == 'Препараты':
            self.medicine_form = medicine_window(self)
            self.medicine_form.ui.pushButton.clicked.connect(self.medicine_form.create_medicine)
            self.medicine_form.exec()
        elif current_table == 'Заказы':
            self.orders_form = orders_window(self)
            self.orders_form.ui.pushButton.clicked.connect(self.orders_form.create_order)
            # Заполняем комбобоксы данными из связанных таблиц
            self.orders_form.load_combo_boxes()
            self.orders_form.exec()

    def open_update_form(self):
        current_table = self.ui.comboBox.currentText()
        current_row = self.ui.tableWidget.currentRow()
        
        if current_row < 0:
            return
            
        if current_table == 'Оптовые_клиенты':
            self.client_form = client_window(self)
            if hasattr(self, 'client_data') and current_row < len(self.client_data):
                client_data = self.client_data[current_row]
                self.client_form.inn = client_data[0]
                
                # Заполняем поля формы
                self.client_form.ui.lineEdit.setText(str(client_data[0]))  
                self.client_form.ui.lineEdit_2.setText(str(client_data[1]))  
                self.client_form.ui.lineEdit_3.setText(str(client_data[2]))  
                self.client_form.ui.lineEdit_4.setText(str(client_data[3]))  
                self.client_form.ui.lineEdit_5.setText(str(client_data[4]))  

                self.client_form.ui.pushButton.clicked.connect(self.client_form.update_client)
                self.client_form.exec()
                
        elif current_table == 'Препараты':
            self.medicine_form = medicine_window(self)
            if hasattr(self, 'medicine_data') and current_row < len(self.medicine_data):
                medicine_data = self.medicine_data[current_row]
                self.medicine_form.inn = medicine_data[0]
                
                # Заполняем поля формы
                self.medicine_form.ui.lineEdit.setText(str(medicine_data[0]))   
                self.medicine_form.ui.lineEdit_2.setText(str(medicine_data[1])) 
                self.medicine_form.ui.lineEdit_3.setText(str(medicine_data[2])) 
                self.medicine_form.ui.lineEdit_4.setText(str(medicine_data[3])) 
                self.medicine_form.ui.lineEdit_5.setText(str(medicine_data[4])) 
                self.medicine_form.ui.lineEdit_6.setText(str(medicine_data[5])) 

                self.medicine_form.ui.pushButton.clicked.connect(self.medicine_form.update_medicine)
                self.medicine_form.exec()
                
        elif current_table == 'Заказы':
            self.orders_form = orders_window(self)
            if hasattr(self, 'orders_data') and current_row < len(self.orders_data):
                orders_data = self.orders_data[current_row]
                self.orders_form.inn = orders_data[0]
                
                # Загружаем данные для комбобоксов
                self.orders_form.load_combo_boxes()
                
                # Заполняем поля формы
                self.orders_form.ui.comboBox.setCurrentIndex(self.orders_form.find_combo_index_by_client_id(orders_data[1]))
                self.orders_form.ui.comboBox_2.setCurrentIndex(self.orders_form.find_combo_index_by_medicine_id(orders_data[2]))
                self.orders_form.ui.dateEdit.setDate(QDate.fromString(orders_data[3], 'yyyy-MM-dd'))
                self.orders_form.ui.lineEdit.setText(str(orders_data[4]))  # Количество
                self.orders_form.ui.lineEdit_2.setText(str(orders_data[5]))  # Скидка

                self.orders_form.ui.pushButton.clicked.connect(self.orders_form.update_order)
                self.orders_form.exec()

    def delete_row(self):
        current_table = self.ui.comboBox.currentText()
        current_row = self.ui.tableWidget.currentRow()
        print(current_row)
        
        if current_row < 0:
            QMessageBox.warning(self, "Внимание", "Выберите запись для удаления")
            return
        
        record_id = None
        table_name = ""
        id_field = ""
        
        if current_table == 'Оптовые_клиенты':
            if hasattr(self, 'client_data') and current_row < len(self.client_data):
                record_id = self.client_data[current_row][0]
                table_name = "Оптовые_клиенты"
                id_field = "client_number"
        elif current_table == 'Препараты':
            if hasattr(self, 'medicine_data') and current_row < len(self.medicine_data):
                record_id = self.medicine_data[current_row][0]
                table_name = "Препараты"
                id_field = "medicine_code"
        elif current_table == 'Заказы':
            if hasattr(self, 'orders_data') and current_row < len(self.orders_data):
                record_id = self.orders_data[current_row][0]
                table_name = "Заказы"
                id_field = "order_number"
        
        if record_id is None:
            QMessageBox.warning(self, "Ошибка", "Не удалось определить запись для удаления")
            return
        
        reply = QMessageBox.question(
            self, 
            "Подтверждение удаления", 
            f"Вы действительно хотите удалить запись?\nЭто действие нельзя отменить.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                cursor.execute(f'DELETE FROM "{table_name}" WHERE {id_field} = ?', (record_id,))
                conn.commit()
                
                if current_table == 'Оптовые_клиенты':
                    self.read_clients()
                elif current_table == 'Препараты':
                    self.read_medicine()
                elif current_table == 'Заказы':
                    self.read_orders()
                
                QMessageBox.information(self, "Успех", "Запись успешно удалена")
                
            except Exception as e:
                print(f"Ошибка при удалении: {e}")
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить запись: {str(e)}")


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
            QMessageBox.critical(self, 'Действие не выполнено', 'Заполните все поля', QMessageBox.Ok)
            return
        q = QMessageBox.critical(self, 'Подтвердите действие', 'Вы действительно хотите изменить запись?',
                                 QMessageBox.Ok|QMessageBox.Cancel)
        if q == QMessageBox.Ok:
            try:
                cursor.execute('INSERT INTO Оптовые_клиенты VALUES(NULL,?,?,?,?)', client_data)
                conn.commit()
                main_form.read_clients()
                return
            except:
                QMessageBox.critical(self, 'Ошибка', 'Ошибка редактирования', QMessageBox.Ok)

    def update_client(self):
        client_id = self.inn
        client_data = [
                       self.ui.lineEdit_2.text(),
                       self.ui.lineEdit_3.text(),
                       self.ui.lineEdit_4.text(),
                       self.ui.lineEdit_5.text()]
        if any([item == '' for item in client_data]):
            QMessageBox.critical(self, 'Действие не выполнено', 'Заполните все поля', QMessageBox.Ok)
            return
        q = QMessageBox.critical(self, 'Подтвердите действие', 'Вы действительно хотите изменить запись?',
                                 QMessageBox.Ok|QMessageBox.Cancel)
        if q == QMessageBox.Ok:
            try:
                cursor.execute(f'UPDATE Оптовые_клиенты SET surname = ?, name = ?, patronymic = ?, city = ? WHERE client_number = {client_id}', client_data)
                conn.commit()
                main_form.read_clients()
                return
            except:
                QMessageBox.critical(self, 'Ошибка', 'Ошибка редактирования', QMessageBox.Ok)


class medicine_window(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = medicineUI()
        self.ui.setupUi(self)

    def create_medicine(self):
        client_data = [
                       self.ui.lineEdit_2.text(),
                       self.ui.lineEdit_3.text(),
                       self.ui.lineEdit_4.text(),
                       self.ui.lineEdit_5.text(),
                       self.ui.lineEdit_6.text()]
        if any([item == '' for item in client_data]):
            QMessageBox.critical(self, 'Действие не выполнено', 'Заполните все поля', QMessageBox.Ok)
            return
        q = QMessageBox.critical(self, 'Подтвердите действие', 'Вы действительно хотите изменить запись?',
                                 QMessageBox.Ok|QMessageBox.Cancel)
        if q == QMessageBox.Ok:
            try:
                cursor.execute('INSERT INTO Препараты VALUES(NULL,?,?,?,?,?)', client_data)
                conn.commit()
                main_form.read_medicine()
                return
            except:
                QMessageBox.critical(self, 'Ошибка', 'Ошибка редактирования', QMessageBox.Ok)

    def update_medicine(self):
        medicine_id = self.inn
        medicine_data = [
                       self.ui.lineEdit_2.text(),
                       self.ui.lineEdit_3.text(),
                       self.ui.lineEdit_4.text(),
                       self.ui.lineEdit_5.text(),
                       self.ui.lineEdit_6.text()]
        if any([item == '' for item in client_data]):
            QMessageBox.critical(self, 'Действие не выполнено', 'Заполните все поля', QMessageBox.Ok)
            return
        q = QMessageBox.critical(self, 'Подтвердите действие', 'Вы действительно хотите изменить запись?',
                                 QMessageBox.Ok|QMessageBox.Cancel)
        if q == QMessageBox.Ok:
            try:
                cursor.execute(f'UPDATE Препараты SET name = ?, origin_country = ?, pack = ?, price = ?, certificate = ? WHERE medicine_number = {medicine_id}', medicine_data)
                conn.commit()
                main_form.read_medicine()
                return
            except:
                QMessageBox.critical(self, 'Ошибка', 'Ошибка редактирования', QMessageBox.Ok)

class orders_window(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = ordersUI()
        self.ui.setupUi(self)

        self.client_data = []
        self.medicine_data = []

    def load_combo_boxes(self):
        # Загружаем список клиентов
        cursor.execute('SELECT client_number, surname, name FROM Оптовые_клиенты')
        self.client_data = cursor.fetchall()
        self.ui.comboBox.clear()
        for client in self.client_data:
            self.ui.comboBox.addItem(f"{client[1]} {client[2]} (ID: {client[0]})", client[0])
        
        # Загружаем список препаратов
        cursor.execute('SELECT medicine_code, name FROM Препараты')
        self.medicine_data = cursor.fetchall()
        self.ui.comboBox_2.clear()
        for medicine in self.medicine_data:
            self.ui.comboBox_2.addItem(f"{medicine[1]} (ID: {medicine[0]})", medicine[0])
        
        # Устанавливаем текущую дату
        self.ui.dateEdit.setDate(QDate.currentDate())

    def find_combo_index_by_client_id(self, client_id):
        for i in range(self.ui.comboBox.count()):
            if self.ui.comboBox.itemData(i) == client_id:
                return i
        return 0

    def find_combo_index_by_medicine_id(self, medicine_id):
        for i in range(self.ui.comboBox_2.count()):
            if self.ui.comboBox_2.itemData(i) == medicine_id:
                return i
        return 0

    def create_order(self):
        client_data = [
                       self.ui.comboBox.currentData(),
                       self.ui.comboBox_2.currentData(),
                       self.ui.dateEdit.date().toString('yyyy-MM-dd'),
                       self.ui.lineEdit_2.text(),
                       self.ui.lineEdit_3.text()]
        if any([item == '' for item in client_data]):
            QMessageBox.critical(self, 'Действие не выполнено', 'Заполните все поля', QMessageBox.Ok)
            return
        q = QMessageBox.critical(self, 'Подтвердите действие', 'Вы действительно хотите изменить запись?',
                                 QMessageBox.Ok|QMessageBox.Cancel)
        if q == QMessageBox.Ok:
            try:
                cursor.execute('INSERT INTO Заказы VALUES(NULL,?,?,?,?,?)', client_data)
                conn.commit()
                main_form.read_orders()
                return
            except:
                QMessageBox.critical(self, 'Ошибка', 'Ошибка редактирования', QMessageBox.Ok)

    def update_order(self):
        order_id = self.inn
        order_data = [
                       self.ui.comboBox.currentData(),
                       self.ui.comboBox_2.currentData(),
                       self.ui.dateEdit.date().toString('yyyy-MM-dd'),
                       self.ui.lineEdit_2.text(),
                       self.ui.lineEdit_3.text()]
        if any([item == '' for item in client_data]):
            QMessageBox.critical(self, 'Действие не выполнено', 'Заполните все поля', QMessageBox.Ok)
            return
        q = QMessageBox.critical(self, 'Подтвердите действие', 'Вы действительно хотите изменить запись?',
                                 QMessageBox.Ok|QMessageBox.Cancel)
        if q == QMessageBox.Ok:
            try:
                cursor.execute(f'UPDATE Заказы SET client_number = ?, medicine_code = ?, date = ?, quantity = ?, sale = ? WHERE order_number = {order_id}', order_data)
                conn.commit()
                main_form.read_orders()
                return
            except:
                QMessageBox.critical(self, 'Ошибка', 'Ошибка редактирования', QMessageBox.Ok)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.png'))
    conn = sqlite3.connect('Микстура.db')  
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    window = LoginWindow() #Создание окна авторизации
    window.show()
    result = app.exec_()
    sys.exit(app.exec_())  
    cursor.close()  
    conn.close()
