from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, CheckConstraint, Float
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


class Publisher(Base):
    """Represents a publisher in the database."""
    __tablename__ = 'publisher'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

    def __str__(self):
        return f'Publisher: {self.name}'

    def __repr__(self):
        return f'Publisher(id={self.id}, name="{self.name}")'


class Book(Base):
    """Represents a book in the database."""
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    id_publisher = Column(Integer, ForeignKey('publisher.id'))
    publisher = relationship(Publisher)

    def __str__(self):
        return f'Book: {self.title} (Publisher: {self.publisher.name})'

    def __repr__(self):
        return f'Book(id={self.id}, title="{self.title}", publisher_id={self.id_publisher})'


class Shop(Base):
    """Represents a shop in the database."""
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

    def __str__(self):
        return f'Shop: {self.name}'

    def __repr__(self):
        return f'Shop(id={self.id}, name="{self.name}")'


class Stock(Base):
    """Represents a stock of books in a shop."""
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'))
    id_shop = Column(Integer, ForeignKey('shop.id'))
    count = Column(Integer, nullable=False)
    book = relationship(Book)
    shop = relationship(Shop)

    __table_args__ = (
        CheckConstraint('count >= 0', name='ck_stock_count_positive'),
    )

    def __str__(self):
        return f'Stock: {self.book.title} in {self.shop.name} (count: {self.count})'

    def __repr__(self):
        return f'Stock(id={self.id}, book_id={self.id_book}, shop_id={self.id_shop}, count={self.count})'


class Sale(Base):
    """Represents a sale of a book."""
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    date_sale = Column(DateTime)
    count = Column(Integer, nullable=False)
    id_stock = Column(Integer, ForeignKey('stock.id'))
    stock = relationship(Stock)

    __table_args__ = (
        CheckConstraint('count >= 0', name='ck_stock_count_positive'),
    )

    def __str__(self):
        return f'Sale: {self.stock.book.title} on {self.date_sale} (price: {self.price})'

    def __repr__(self):
        return f'Sale(id={self.id}, stock_id={self.id_stock}, price={self.price}, date_sale="{self.date_sale}")'

