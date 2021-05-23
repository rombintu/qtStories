import os
import ipaddress
import form
import sys
import socket                   # Import socket module

from PyQt5 import QtWidgets, uic

s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
port = 60001                    # Reserve a port for your service.



def valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False
    else:
        return True

class App(QtWidgets.QMainWindow, form.Ui_MainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.setupUi(self)
        
        ip, yes = QtWidgets.QInputDialog.getText(self, 'Вход', 'Введи ip сервера:')
        if yes and valid_ip(ip) or ip == 'localhost':
            s.connect((ip, port))
            data = s.recv(1024)
            s.close()
            print(data.decode())
            print('connection closed')
            
        else:
            print('Неправильный адрес сервера')
            sys.exit()


# MAIN
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = App()
    win.show()
    app.exec_()