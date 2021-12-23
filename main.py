from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from booking_service.front import (
    get_user_registration_data, get_table_data, get_confirmation,
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


@app.get('/')
async def root():
    return {"message": "Hello World!"}


@app.get('/confirmation')
async def confirmation():
    send_booking_data()
    confirmation_response = get_confirmation()
    if confirmation_response is True:
        return {"message": "Cool"}
    return {"message": "Not Cool"}


@app.get('/book')
async def booking():
    table_data = get_table_data()
    crud.book_table(table_data)


@app.get('/registration')
async def registration(db: Session = Depends(get_db)):
    user_data = get_user_registration_data()
    db_user = crud.get_user_by_phone(db, user_data.phone)
    crud.create_user(db, user_data)
    response = RedirectResponse('/book')
    return response


if __name__ == "__main__":
    ...
