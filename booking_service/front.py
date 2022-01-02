from typing import List
from pywebio.input import input_group, input, select

from booking_service.schemas import User, Table
import booking_service.models as models


def get_user_registration_data():
    # user_data = input_group(
    #     "Регистрация",
    #     [
    #         input('Телефон', name='phone'),
    #         input('Имя', name='name'),
    #         input('Количество человек', name='number_of_persons'),
    #         input('Номер столика', name='table_id'),
    #         input('Время брони', name='booking_time'),
    #     ]
    # )
    # return User(
    #     id=1,
    #     phone=user_data['phone'],
    #     name=user_data['name'],
    #     number_of_persons=user_data['number_of_persons'],
    #     table_id=user_data['table_id'],
    #     booking_time=user_data['booking_time'],
    # )
    return User(
        id=1,
        phone='392308239823',
        name='Vlad',
        number_of_persons=2,
        table_id=1,
        booking_time=60,
    )


def table_info(table: models.Table):
    return f'{table.id}: Столик на {table.capacity}, цена в час - {table.price_per_hour}'


def get_choosed_table_id(free_tables: List[models.Table]):
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
    # return 1


def send_booking_data():
    ...


def get_confirmation():
    ...
