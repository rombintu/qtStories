import os
import json
import ipaddress

import socket                   # Import socket module
import config

# s = socket.socket()             # Create a socket object
port = config.PORT
# host = config.HOST
from common import send_msg, recv_msg
# ECP
import sign

# Переменные для файлов
tmp = os.getcwd() + '/tmp'
storyfile = tmp + '/stories.json'
signfile = tmp + '/signature.pem'
keyfile = tmp + '/key.pem'

def writefile(filename, content):
    with open(filename, 'wb') as f:
        f.write(content.encode())
        
# Функция для проверки валидности айпи
def valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False
    else:
        return True

# Получение контента по именам из файла, например get_content('hero')
def get_content(name):
    name_arr = []
    with open(storyfile, 'r') as f:
        data = json.loads(f.read())
    arr = data['data']
    for el in arr:
        name_arr.append(el[name])
    return name_arr

# Подключение к серверу и скачивание нового файла джейсон
def update_base(ip):
    with socket.socket() as sock:
        sock.connect((ip, port))
        for file_name in [storyfile, signfile, keyfile]:
            print('receiving data...')
            data = recv_msg(sock.recv(1024))
            # write data to a storyfile
            # file_name.write(data)
            print(data)
        print('Successfully get the storyfile')
        print('connection closed')

def checker():
    return sign.check_sign(storyfile, keyfile, signfile)