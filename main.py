# -*- coding: utf-8 -*-
import datetime
import pyqrcode
from fastapi import FastAPI
from pywebio.platform.fastapi import webio_routes
from fastapi_utils.tasks import repeat_every

from booking_service.front import (
    get_user_registration_data, get_choosed_table_id, put_confirmation,
    get_booking_time, time_table, get_duration_of_booking
)
from booking_service import crud, models
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
    if order:
        order = crud.check_order(db, order.id)
        text = f"You booked desk: {order.desk_id} at {order.booking_time} for {order.duration_of_booking}h"
    else:
        text = "Has no booked tables."
    return text


def get_host_url():
    return "http://127.0.0.1:8000/"


@app.on_event('startup')
@repeat_every(seconds=60)
def unbooking_tables():
    db = get_db()
    db_orders = crud.get_orders(db)
    current_time = datetime.datetime.now()
    for db_order in db_orders:
        db_order_time = datetime.datetime.strptime(db_order.booking_time, '%Y-%m-%d %H:%M:%S')
        if db_order_time + datetime.timedelta(minutes=15) <= current_time \
                and not db_order.checked:
            crud.cancel_booking(db, db_order.booker_id)


def main():
    db = get_db()
    user_data = get_user_registration_data()
    db_user = crud.get_user_by_phone(db, user_data.phone)
    if db_user is None:
        db_user = crud.create_user(db, user_data)
    order_by_user = crud.get_order_by_booker_id(db, db_user.id)

    if order_by_user is None:
        free_tables = crud.get_free_tables(db)
        table_id = get_choosed_table_id(free_tables)
        booking_time = get_booking_time()
        duration_of_booking = int(get_duration_of_booking())
        order_by_user = crud.book_desk(
            db, table_id, db_user.id,
            time_table[booking_time], duration_of_booking
        )
    url = get_host_url() + "check/" + str(order_by_user.id)
    qrcode = pyqrcode.create(url)
    qrcode.png('resources/user.png', scale=20)
    put_confirmation(open('resources/user.png', 'rb').read())


app.mount('/', FastAPI(routes=webio_routes(main)))

if __name__ == "__main__":
    main()
