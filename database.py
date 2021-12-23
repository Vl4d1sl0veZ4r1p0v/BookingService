from sqlalchemy import Column, Integer, String, Float, Time
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import PhoneNumber

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    phone = Column(PhoneNumber)
    number_of_persons = Column(Integer)
    id_table = Column(Integer)
    booking_time = Column(Time)


class Table(Base):
    __tablename__ = 'table'
    id = Column(Integer, primary_key=True)
    capacity = Column(Integer)
    price_by_place = Column(Float)


class DBAdapter:
    def __init__(self):
        ...

    def put_user_data():
        ...

    def book_table():
        ...
