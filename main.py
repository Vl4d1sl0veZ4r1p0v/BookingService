from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from front import (
    get_user_data, get_table_data, get_confirmation,
    send_booking_data
)
from database import put_user_data, book_table

app = FastAPI()


class UserData(BaseModel):
    phone_number: str
    firstname: str
    lastname: str


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
    book_table(table_data)


@app.get('/registration')
async def registration():
    user_data = get_user_data()
    put_user_data(user_data)
    response = RedirectResponse('/book')
    return response


if __name__ == "__main__":
    ...
