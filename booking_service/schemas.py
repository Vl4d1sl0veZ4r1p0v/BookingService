from typing import Optional
from pydantic import BaseModel


class TableBase(BaseModel):
    capacity: int


class TableCreate(TableBase):
    pass


class Table(TableBase):
    id: int
    price_per_place: float
    booker_id: int


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
