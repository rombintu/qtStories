from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import json

DeclarativeBase = declarative_base()

class Stories(DeclarativeBase):
    __tablename__ = "stories"

    id = Column('id', Integer, primary_key=True)
    hero = Column('hero', String)
    story = Column('story', String)
    end = Column('end', String)

    def __init__(self, hero, story, end):
        self.hero = hero
        self.story = story
        self.end = end

def add_stories(file_name="add_story.json"):
    #Создаем объект Engine, который будет использоваться объектами ниже для связи с БД
    # engine = create_engine('postgresql://test:password@localhost:5432/project13')
    engine = create_engine('sqlite:///db.sqlite')
    #Метод create_all создает таблицы в БД , определенные с помощью  DeclarativeBase
    DeclarativeBase.metadata.create_all(engine)
    # Создаем фабрику для создания экземпляров Session. Для создания фабрики в аргументе 
    # bind передаем объект engine
    Session = sessionmaker(bind=engine)
    # Создаем объект сессии из вышесозданной фабрики Session
    session = Session()

    def get_stories():
        with open(file_name, 'r') as f:
            stories = json.loads(f.read())
        return stories['hero'], stories['story'], stories['end']
    
    stories = get_stories()
    new_horror = Stories(stories[0], stories[1], stories[2])
    session.add(new_horror)
    session.commit()
    session.close()

    print('Новая история добавлена в базу данных.')
    
if __name__ == "__main__":
    add_stories()