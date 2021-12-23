from booking_service.schemas import User, Table


def get_user_data():
    return User(
        id=1,
        phone='392308239823',
        name='Vlad',
        number_of_persons=2,
        table_id=1,
        booking_time=60,
    )


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
