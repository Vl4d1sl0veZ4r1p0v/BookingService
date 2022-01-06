from sqlalchemy import (Column, ForeignKey, Integer, String, Float,
                        DateTime, UniqueConstraint, Boolean)
from booking_service.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String)
    name = Column(String)
    __table_args__ = (UniqueConstraint('phone', name='_user_phone_uc'),)


class Desk(Base):
    __tablename__ = 'desks'

    id = Column(Integer, primary_key=True, index=True)
    capacity = Column(Integer)
    price_per_hour = Column(Float)


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    booking_time = Column(String)
    duration_of_booking = Column(Integer)
    booker_id = Column(Integer, ForeignKey('users.id'))
    desk_id = Column(Integer, ForeignKey('desks.id'))
    checked = Column(Boolean, default=False)
