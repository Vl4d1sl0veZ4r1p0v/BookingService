from sqlalchemy import Column, ForeignKey, Integer, String, Float
from booking_service.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String)
    name = Column(String)
    number_of_persons = Column(Integer)
    table_id = Column(Integer, ForeignKey('tables.id'))
    booking_time = Column(Integer)  # Задается в минутах


class Table(Base):
    __tablename__ = 'tables'

    id = Column(Integer, primary_key=True, index=True)
    capacity = Column(Integer)
    price_per_place = Column(Float)
    booker_id = Column(Integer, ForeignKey('users.id'))
