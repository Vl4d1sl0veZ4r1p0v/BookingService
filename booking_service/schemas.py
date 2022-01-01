# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel


class Table(BaseModel):
    id: int
    capacity: int
    price_per_hour: float  # Переделал, так как мы бронируем весь столик, нет смысла каждое место отдельно рассмаривать
    booker_id: Optional[int]  # Нужно, так как столик может быть не забронированным.


class UserBase(BaseModel):
    phone: str
    name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    number_of_persons: Optional[int] = None
    table_id: int
    booking_time: int
