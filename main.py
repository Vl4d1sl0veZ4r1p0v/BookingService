# -*- coding: utf-8 -*-
import pyqrcode
from fastapi import FastAPI
from time import time
from pywebio.platform.fastapi import webio_routes
from fastapi_utils.tasks import repeat_every

from booking_service.front import (
    get_user_registration_data, get_choosed_table_id, put_confirmation,
    get_booking_time, time_table, get_duration_of_booking
)
from booking_service import crud, models, schemas
from booking_service.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


@app.get("/check/{order_id}")
def check(order_id):
    db = get_db()
    order = crud.get_order_by_id(db, order_id)
    order = crud.check_order(db, order.id)
    if order:
        text = f"You booked desk: {order.desk_id} at {order.booking_time} for {order.duration_of_booking}h"
    else:
        text = "Has no booked tables."
    return text


def get_host_url():
    return "http://127.0.0.1:8000/"


# @repeat_every(60)
# def unbooking_tables():
#     ...


def main():
    db = get_db()

    user_data = get_user_registration_data()
    # user_data = schemas.User(id=3, phone='+79122918215', name='Vova')
    db_user = crud.get_user_by_phone(db, user_data.phone)
    if db_user is None:
        db_user = crud.create_user(db, user_data)
    order_by_user = crud.get_order_by_booker_id(db, db_user.id)

    if order_by_user is None:
        free_tables = crud.get_free_tables(db)
        table_id = get_choosed_table_id(free_tables)
        table_id = 2
        booking_time = get_booking_time()
        booking_time_id = time_table[booking_time]
        duration_of_booking = int(get_duration_of_booking())
        order_by_user = crud.book_desk(
            db, table_id, db_user.id,
            time_table[booking_time], duration_of_booking
        )
    url = get_host_url() + "check/" + str(order_by_user.id)
    print(url)
    qrcode = pyqrcode.create(url)
    qrcode.png('user.png', scale=20)
    put_confirmation(open('user.png', 'rb').read())


app.mount('/', FastAPI(routes=webio_routes(main)))


if __name__ == "__main__":
    main()
