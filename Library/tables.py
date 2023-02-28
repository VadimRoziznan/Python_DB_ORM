import sqlalchemy as sq
import psycopg2

from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Publisher(Base):

    __tablename__ = 'publisher'

    id_publisher = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), unique=True, nullable=False)

    def __str__(self):
        return f'{self.id_publisher}, {self.name}'


class Book(Base):

    __tablename__ = 'book'

    id_book = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=60), nullable=False)
    id_publisher = sq.Column(
        sq.Integer, sq.ForeignKey('publisher.id_publisher'), nullable=False
    )

    publisher = relationship(Publisher, backref='book')

    def __str__(self):
        return f'{self.id_book}, {self.title}, {self.id_publisher}'


class Shop(Base):

    __tablename__ = 'shop'

    id_shop = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), unique=True, nullable=False)

    def __str__(self):
        return f'{self.id_shop}, {self.name}'


class Stock(Base):

    __tablename__ = 'stock'

    id_stock = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(
        sq.Integer, sq.ForeignKey('book.id_book'), nullable=False
    )
    id_shop = sq.Column(
        sq.Integer, sq.ForeignKey('shop.id_shop'), nullable=False
    )
    count = sq.Column(sq.Integer, nullable=False)

    book = relationship(Book, backref='stock')
    shop = relationship(Shop, backref='stock')

    def __str__(self):
        return f'{self.id_stock}, {self.id_book}, {self.id_shop}, {self.count}'


class Sale(Base):

    __tablename__ = 'sale'

    id_sale = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric, nullable=False)
    date_sale = sq.Column(sq.TIMESTAMP, nullable=False)
    id_stock = sq.Column(
        sq.Integer, sq.ForeignKey('stock.id_stock'), nullable=False
    )
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stock, backref='sale')

    def __str__(self):
        return f'{self.id_sale}, {self.price}, {self.date_sale}, ' \
               f'{self.id_stock}, {self.count}'


def create_db(user, password, db_name):
    try:
        conn = psycopg2.connect(user=user, password=password)
        with conn.cursor() as cur:
            conn.autocommit = True
            cur.execute(f"CREATE DATABASE {db_name}")
        conn.close()
        return print('База данных создана успешно.')
    except:
        return


def create_tables(engine):
    Base.metadata.create_all(engine)
