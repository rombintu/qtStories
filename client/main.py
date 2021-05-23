import os
import ipaddress
import form
import sys
import socket                   # Import socket module
import json
from random import choice
from PyQt5 import QtWidgets, uic

s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
port = 60001                    # Reserve a port for your service.

file = os.getcwd() + '/stories.json'

def valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False
    else:
        return True

def get_content(name):
    name_arr = []
    with open(file, 'r') as f:
        data = json.loads(f.read())
    arr = data['data']
    for el in arr:
        name_arr.append(el[name])
    return name_arr

def update_base(ip):
    s.connect((ip, port))
    with open(file, 'wb') as f:
        while True:
            print('receiving data...')
            data = s.recv(1024)
            if not data:
                break
            # write data to a file
            f.write(data)

    f.close()
    print('Successfully get the file')
    s.close()
    print('connection closed')


class App(QtWidgets.QMainWindow, form.Ui_MainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.setupUi(self)
        
            
        self.pushButton.clicked.connect(self.update_hero)
        self.pushButton_2.clicked.connect(self.update_story)
        self.pushButton_3.clicked.connect(self.update_end)
        self.pushButton_4.clicked.connect(self.export_json)
        self.pushButton_5.clicked.connect(self.import_json)
        self.pushButton_6.clicked.connect(self.update_stories)
        


    def update_hero(self):
        try:
            arr = get_content('hero')
            self.textBrowser.setText(choice(arr))
        except Exception as e:
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

    def export_json(self):
        pass
    
    def import_json(self):
        pass

    def update_stories(self):
        ip, yes = QtWidgets.QInputDialog.getText(self, 'Вход', 'Введи ip сервера:')
        if yes and valid_ip(ip) or ip == 'localhost':
            try:
                update_base(ip)
            except Exception as e:
                errorWin = QtWidgets.QErrorMessage(self)
                errorWin.showMessage(f'Ошибка: \n{e}')
        else:
            errorWin = QtWidgets.QErrorMessage(self)
            errorWin.showMessage(f'Ошибка: \n{e}')
        
# MAIN
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = App()
    win.show()
    app.exec_()