from typing import List
from pywebio.input import input_group, input, select, radio
from pywebio.output import put_image, get_scope, use_scope, put_button

from booking_service.schemas import User, Table
import booking_service.models as models


def get_user_registration_data():
    user_data = input_group(
        "Регистрация",
        [
            input('Телефон', name='phone'),
            input('Имя', name='name'),
        ]
    )
    return User(
        id=1,
        phone=user_data['phone'],
        name=user_data['name'],
    )


def table_info(table: models.Desk):
    return f'{table.id}: Столик на {table.capacity}, цена в час - {table.price_per_hour}'


def get_choosed_table_id(free_tables: List[models.Desk]):
    table_data = select(
        "Выберите столик",
        list(map(lambda x: table_info(Table(
            id=x.id,
            capacity=x.capacity,
            price_per_hour=x.price_per_hour,
            booker_id=x.booker_id
        )), free_tables))  # Короче, здесь должна быть строка
    )
    return int(table_data[:table_data.find(":")])


def put_confirmation(qrcode_image: bytes):
    put_image(qrcode_image)


def get_booking_time() -> str:
    booking_time = input_group(
        'Время бронирования',
        [
            radio(text) for text in ['hui', 'foo']
        ]
    )
    return booking_time
