# https://ru.wikibooks.org/wiki/SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Берем наш класс (модель таблички с историями)
from model import Stories
# Встроенные либы
import socket    
import json
import os

import config
# ЭЦП
from sign import sign_init

from common import send_msg, recv_msg


# Получаем порт и айпи из переменных окружения (для секьюрности)
port = config.PORT
host = config.HOST
# Создаем сокет
# s = socket.socket()             
# Связываем сокет с адресом и портом
# s.bind((host, port))
# # слушаем сокет для 5 соединений максимум
# s.listen(5)

# Переменная для файла джайсон
tmp = os.getcwd() + '/tmp'
storyfile = tmp + '/stories.json'
signfile = tmp + '/signature.pem'
keyfile = tmp + '/key.pem'

def writefile(filename, content):
    with open(filename, 'wb') as f:
        f.write(content.encode())

def write_pem(content, file):
        with open(file, 'wb') as f:
            f.write(content)

def create_story_file():
    # Если нужна постгря то раскоменчиваем следующую строчку
    # engine = create_engine('postgresql://test:password@localhost:5432/project13')
    engine = create_engine('sqlite:///db.sqlite')
    Session = sessionmaker(bind=engine)
    session = Session()
    # берем все истории
    stories = session.query(Stories).all()

    # сюда кладем данные
    arr_data = []
    for st in stories:
        arr_data.append(
            {"hero": st.hero, 
            "story": st.story,
            "end": st.end})

    # Открываем файл и записываем туда истории
    with open(storyfile, 'w') as f:
        f.write(json.dumps({"data": arr_data}, indent=4))

def create_signature():
    k, s = sign_init(storyfile)
    write_pem(s, signfile)
    write_pem(k, keyfile)
    print('Sign storyfile...')

# def sendfile(filename):
#     f = open(filename,'rb')
#     l = f.read(1024)
#     # Отправляем по 1024 байт
#     while (l):
#         conn.send(l)
#         l = f.read(1024)
#     f.close()

def readfile(filename):
    with open(filename, 'rb') as f:
        return f.read()

# Главная функция
def main():
    print('Server is started...')
    create_story_file()
    create_signature()
    for file_name in [storyfile, signfile, keyfile]:
        with socket.socket() as sock:
            sock.bind((host, port))
            sock.listen()
            # Все делаем в цикле (типа сервер слушает соединения)
            while True:
                # Когда кто то присоединяется то берем данные о клиенте
                conn, addr = sock.accept()
                # Есть с кем то соединение то берем данные из бд
                
                data = readfile(file_name)
                send_msg(sock, data)
                print(f'Done sending to {addr} file {file_name}')
                # Закрываем соединение
            
if __name__ == "__main__":
    main()