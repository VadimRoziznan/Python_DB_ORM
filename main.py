import configparser
import sqlalchemy as sq
import sys
import os

sys.path.append(os.path.join('..'))
from sqlalchemy.orm import sessionmaker
from Library.load_json_db import load_json_db
from Library.tables import create_tables, Publisher, Book, Shop, Stock, Sale, \
    create_db

config = configparser.ConfigParser()
config.read("settings.ini")
driver = config["settings"]["driver"]
login = config["settings"]["login"]
password = config["settings"]["password"]
db_name = config["settings"]["db_name"]

create_db(login, password, db_name)

engine = sq.create_engine(f'{driver}://{login}:{password}@localhost:5432/'
                          f'{db_name}')

create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()
question = input('Заполнить БД тестовыми данными? ').lower()
if question in ['да', 'yes', 'lf', 'нуы']:
    load_json_db(session)
while True:
    question = input('Введите издателя: ')
    if question in ['Выход', 'Exit']:
        break
    if question not in [
        publisher.name for publisher in session.query(Publisher)
    ]:
        print('Издатель не найден.')
        continue
    subq = session.query(Publisher).filter(Publisher.name.like(
        f'{question}')).subquery()
    for book, shop, sale in session.query(Book, Shop, Sale).\
            join(subq, Book.id_publisher == subq.c.id_publisher).\
            join(Stock, Book.id_book == Stock.id_book).\
            join(Shop, Stock.id_shop == Shop.id_shop).\
            join(Sale, Stock.id_stock == Sale.id_stock).\
            all():
        print(f'{book.title} | {shop.name} | {sale.price * sale.count} |'
              f' {sale.date_sale}')

session.close()
