# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel


class Table(BaseModel):
    id: int
    capacity: int
    price_per_hour: float  # Переделал, так как мы бронируем весь столик, нет смысла каждое место отдельно рассмаривать
    booker_id: Optional[int]  # Нужно, так как столик может быть не забронированным.
    checksum: Optional[int]


class User(BaseModel):
    id: int
    phone: str  # Имеет смысл делать id - номер телефона, чтобы не было несколько пользователей с одним номером.
    name: str
