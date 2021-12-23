from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
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
        yield db
    finally:
        db.close()


def root():
    return {"message": "Hello World!"}


def confirmation():
    send_booking_data()
    confirmation_response = get_confirmation()
    if confirmation_response is True:
        return {"message": "Cool"}
    return {"message": "Not Cool"}


def booking(db: Session = Depends(get_db)):
    user_id = 1
    free_tables = crud.get_free_tables(db)
    table_id = get_choosed_table_id(free_tables)
    crud.book_table(table_id, user_id)


def registration(db: Session = Depends(get_db)):
    user_data = get_user_registration_data()
    db_user = crud.get_user_by_phone(db, user_data.phone)
    crud.create_user(db, user_data)
    response = RedirectResponse('/book')
    return response


app.mount('/', FastAPI(routes=webio_routes(root)))
app.mount('/registration', FastAPI(routes=webio_routes(registration)))
