from sqlalchemy import Table, Column, Integer, String, MetaData



metadata = MetaData()

users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String),
              Column('age', Integer)
              )

metadata.create_all(engine)  # Створення таблиці в базі даних

