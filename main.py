# -*- coding: utf-8 -*-
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pywebio.platform.fastapi import webio_routes

from booking_service.front import (
    get_user_registration_data, get_choosed_table_id, get_confirmation,
    send_booking_data
)
from booking_service import crud, models
from booking_service.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


def confirmation():
    send_booking_data()
    confirmation_response = get_confirmation()
    if confirmation_response is True:
        return {"message": "Cool"}
    return {"message": "Not Cool"}


def booking():
    user_id = 1
    free_tables = crud.get_free_tables()
    table_id = get_choosed_table_id(free_tables)
    crud.book_table(table_id, user_id)


def registration(db: Session):
    user_data = get_user_registration_data()
    db_user = crud.get_user_by_phone(db, user_data.phone)
    crud.create_user(db, user_data)


def main():
    db = get_db()

    # кейс, когда пользователь попадает сразу на страницу регистрации
    # и вводит свои данные
    # user_data = get_user_registration_data()
    # db_user = crud.get_user_by_phone(db, user_data.phone)
    # crud.create_user(db, user_data)

    # пользователь зарегистрирован, нужно прикрепить столик за его id в бд.
    user_id = 1  # Как получить id пользователя из бд?
    free_tables = crud.get_free_tables(db)
    table_id = get_choosed_table_id(free_tables)
    crud.book_table(db, table_id, user_id)
    # нужно, чтобы пользователю возвращялся идентификатор подтверждения, что он тот, кем представляется.

    # панель добавления новых столиков в базу.
    # но это, ведь, совсем не обязательно! базу можно наполнять первое время и руками.


app.mount('/', FastAPI(routes=webio_routes(main)))

if __name__ == "__main__":
    main()
