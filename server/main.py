# https://ru.wikibooks.org/wiki/SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Берем наш класс (модель таблички с историями)
from model import Stories
# Встроенные либы
import socket    
import json
import os

# Получаем порт и айпи из переменных окружения (для секьюрности)
port = os.environ['PORT']
host = os.environ['HOST']
# Создаем сокет
s = socket.socket()             
# Связываем сокет с адресом и портом
s.bind((host, port))
# слушаем сокет для 5 соединений максимум
s.listen(5)
# Переменная для файла джайсон
file = os.getcwd() + '/stories.json'

# Главная функция
def main():
    print('Server is started...')
    # Все делаем в цикле (типа сервер слушает соединения)
    while True:
        # Когда кто то присоединяется то берем данные о клиенте
        conn, addr = s.accept()
        # Есть с кем то соединение то берем данные из бд
        if conn:
            # Если нужна постгря то раскоменчиваем следующую строчку
            # engine = create_engine('postgresql://test:password@localhost:5432/project13')
            engine = create_engine('sqlite:///db.sqlite')
            Session = sessionmaker(bind=engine)
            session = Session()
            # берем все истории
            stories = session.query(Stories).all()
            # сюда положим данные
            arr_data = []
            # Открываем файл и записываем туда истории
            with open(file, 'w') as f:
                for st in stories:
                    arr_data.append(
                        {"hero": st.hero, 
                        "story": st.story,
                        "end": st.end})
                f.write(json.dumps({"data": arr_data}, indent=4))
        # Открываем этот файл для записи и читаем побайтово
        f = open(file,'rb')
        l = f.read(1024)
        # Отправляем по 1024 байт
        while (l):
            conn.send(l)
            l = f.read(1024)
        f.close()

        print(f'Done sending to {addr}')
        # Закрываем соединение
        conn.close()
    

if __name__ == "__main__":
    main()