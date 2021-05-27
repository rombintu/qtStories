import os
import ipaddress
import form
import sys

import json
from random import choice
from PyQt5 import QtWidgets, uic



from func import *


# Окно приложения
class App(QtWidgets.QMainWindow, form.Ui_MainWindow):
    # Инициализация
    def __init__(self):
        super(App, self).__init__()
        self.setupUi(self)
        
        # Коннектим кнопки к нужным функциям
        self.pushButton.clicked.connect(self.update_hero)
        self.pushButton_2.clicked.connect(self.update_story)
        self.pushButton_3.clicked.connect(self.update_end)

        self.pushButton_6.clicked.connect(self.update_stories)
        self.pushButton_7.clicked.connect(self.check_signature)

    # Пересобирает (отдает рандомную хар-ку героя)
    def update_hero(self):
        try:
            arr = get_content('hero')
            self.textBrowser.setText(choice(arr))
        except Exception as e:
            # если ошибка то вылетает окошко с ошибкой
            errorWin = QtWidgets.QErrorMessage(self)
            errorWin.showMessage(f'Ошибка: \n{e}')

    def update_story(self):
        try:
            arr = get_content('story')
            self.textBrowser_2.setText(choice(arr))
        except Exception as e:
            errorWin = QtWidgets.QErrorMessage(self)
            errorWin.showMessage(f'Ошибка: \n{e}')

    def update_end(self):
        try:
            arr = get_content('end')
            self.textBrowser_3.setText(choice(arr))
        except Exception as e:
            errorWin = QtWidgets.QErrorMessage(self)
            errorWin.showMessage(f'Ошибка: \n{e}')


    # Кнопка обновления локальной базы
    def update_stories(self):
        # Спрашиваем у пользователя IP 
        ip, yes = QtWidgets.QInputDialog.getText(self, 'Вход', 'Введи ip сервера:')
        if yes and valid_ip(ip) or ip == 'localhost':
            try:
                update_base(ip)
                self.lineEdit.setText('База обновлена')
                if self.checkBox.checkState():
                    if checker():
                        self.lineEdit.setText('Подпись верна')
                    else:
                        self.lineEdit.setText('Неизвестная подпись')
            except Exception as e:
                errorWin = QtWidgets.QErrorMessage(self)
                errorWin.showMessage(f'Ошибка: \n{e}')
                self.lineEdit.setText('Ошибка')

    def check_signature(self):
        try:
            if checker():
                self.lineEdit.setText('Подпись верна')
            else:
                self.lineEdit.setText('Неизвестная подпись')
        except Exception as e:
            errorWin = QtWidgets.QErrorMessage(self)
            errorWin.showMessage(f'Ошибка: \n{e}')
            self.lineEdit.setText('Ошибка')
        
# MAIN
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = App()
    win.show()
    app.exec_()