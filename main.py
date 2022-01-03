# -*- coding: utf-8 -*-
import pyqrcode
from fastapi import FastAPI
from time import time
from pywebio.platform.fastapi import webio_routes

from booking_service.front import (
    get_user_registration_data, get_choosed_table_id, put_confirmation,
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


#  Так как мы уже не в сессии pywebio, то не можем им пользоваться.
@app.get("/check/{checksum}")
def check(checksum):
    db = get_db()
    booked_tables = crud.get_booked_tables(db, checksum)
    if len(booked_tables) > 0:
        text = ' '.join(map(str, list(map(lambda x: (x.id, x.booker_id), booked_tables))))
    else:
        text = "Has no booked tables."
    return text


def get_host_url():
    return "http://127.0.0.1:8000/"


def main():
    db = get_db()

    # кейс, когда пользователь попадает сразу на страницу регистрации
    # и вводит свои данные
    user_data = get_user_registration_data()
    db_user = crud.create_user(db, user_data)

    # пользователь зарегистрирован, нужно прикрепить столик за его id в бд.
    free_tables = crud.get_free_tables(db)
    table_id = get_choosed_table_id(free_tables)
    checksum = hash(time() + db_user.id)
    crud.book_table(db, table_id, db_user.id, checksum)
    # нужно, чтобы пользователю возвращялся идентификатор подтверждения, что он тот, кем представляется.

    # панель добавления новых столиков в базу.
    # но это, ведь, совсем не обязательно! базу можно наполнять первое время и руками.\

    url = get_host_url() + "check/" + str(checksum)
    print(url)
    qrcode = pyqrcode.create(url)
    qrcode.png('user.png', scale=20)
    put_confirmation(open('user.png', 'rb').read())


app.mount('/', FastAPI(routes=webio_routes(main)))

if __name__ == "__main__":
    main()
