# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel


class Desk(BaseModel):
    id: int
    capacity: int
    price_per_hour: float


class User(BaseModel):
    id: Optional[int]
    phone: str
    name: str
