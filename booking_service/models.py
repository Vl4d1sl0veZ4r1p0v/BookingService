from sqlalchemy import Column, ForeignKey, Integer, String, Float
from booking_service.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String)
    name = Column(String)


class Table(Base):
    __tablename__ = 'tables'

    id = Column(Integer, primary_key=True, index=True)
    capacity = Column(Integer)
    price_per_hour = Column(Float)
    booking_time: int
    booker_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    checksum = Column(Integer, nullable=True)
