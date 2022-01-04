# -*- coding: utf-8 -*-
import pyqrcode
from fastapi import FastAPI
from time import time
from pywebio.platform.fastapi import webio_routes

from booking_service.front import (
    get_user_registration_data, get_choosed_table_id, put_confirmation,
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


@app.get("/check/{checksum}")
def check(checksum):
    db = get_db()
    booked_tables = crud.get_booked_tables_by_checksum(db, checksum)
    if len(booked_tables) > 0:
        text = ' '.join(map(str, list(map(lambda x: (x.id, x.booker_id), booked_tables))))
    else:
        text = "Has no booked tables."
    return text


def get_host_url():
    return "http://127.0.0.1:8000/"


def main():
    db = get_db()

    user_data = get_user_registration_data()
    # user_data = schemas.User(id=1, phone='+79122918214', name='Vlad')
    db_user = crud.get_user_by_phone(db, user_data.phone)
    if db_user is None:
        db_user = crud.create_user(db, user_data)
    tables_booked_by_user = crud.get_booked_tables_by_booker_id(db, db_user.id)
    if len(tables_booked_by_user) == 0:
        free_tables = crud.get_free_tables(db)
        table_id = get_choosed_table_id(free_tables)
        checksum = hash(time() + db_user.id)
        crud.book_table(db, table_id, db_user.id, checksum)
    else:
        checksum = tables_booked_by_user[0].checksum
    url = get_host_url() + "check/" + str(checksum)
    qrcode = pyqrcode.create(url)
    qrcode.png('user.png', scale=20)
    booking_cancel = put_confirmation(open('user.png', 'rb').read())
    if booking_cancel:
        crud.cancel_booking(db, db_user.id)


app.mount('/', FastAPI(routes=webio_routes(main)))

if __name__ == "__main__":
    main()
