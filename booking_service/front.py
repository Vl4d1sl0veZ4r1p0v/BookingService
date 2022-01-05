import booking_service.models as models
import datetime
from typing import List
from pywebio.input import input_group, input, select, radio
from pywebio.output import put_image, get_scope, use_scope, put_button

from booking_service.schemas import User, Desk
from booking_service import friday_datetime

time_table = {
    time_point.strftime('%H:%M'): time_point
    for time_point in [
        friday_datetime + datetime.timedelta(hours=hour) for hour in range(10, 27)
    ]
}


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
        list(map(lambda x: table_info(Desk(
            id=x.id,
            capacity=x.capacity,
            price_per_hour=x.price_per_hour,
        )), free_tables))
    )
    return int(table_data[:table_data.find(":")])


def put_confirmation(qrcode_image: bytes):
    put_image(qrcode_image)


def get_booking_time() -> str:
    booking_time = radio('Время бронирования', options=time_table.keys())
    return booking_time


def get_duration_of_booking() -> int:
    duration_of_booking = select(
        "Выберите продолжительность бронирования",
        [1, 2]
    )
    return duration_of_booking
