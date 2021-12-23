from pywebio.input import input_group, input

from booking_service.schemas import User, Table


def get_user_registration_data():
    user_data = input_group(
        "Регистрация",
        [
            input('Телефон', name='phone'),
            input('Имя', name='name'),
            input('Количество человек', name='number_of_persons'),
            input('Номер столика', name='table_id'),
            input('Время брони', name='booking_time'),
        ]
    )
    return User(
        id=1,
        phone=user_data['phone'],
        name=user_data['name'],
        number_of_persons=user_data['number_of_persons'],
        table_id=user_data['table_id'],
        booking_time=user_data['booking_time'],
    )
    # return User(
    #     id=1,
    #     phone='392308239823',
    #     name='Vlad',
    #     number_of_persons=2,
    #     table_id=1,
    #     booking_time=60,
    # )


def get_table_data():
    return Table(
        id=1,
        capacity=2,
        price_per_place=1000,
        booker_id=1,
    )


def send_booking_data():
    ...


def get_confirmation():
    ...
