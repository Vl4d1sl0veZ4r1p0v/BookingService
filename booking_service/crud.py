import datetime

from sqlalchemy.orm import Session
from booking_service import schemas, models


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_phone(db: Session, user_phone: str):
    return db.query(models.User).filter(models.User.phone == user_phone).first()


def create_user(db: Session, user: schemas.User):
    db_user = models.User(
        phone=user.phone,
        name=user.name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_free_tables(db: Session):
    db_booked_desks = db.query(models.Order.desk_id).all()
    db_booked_desks = list(map(lambda x: x[0], db_booked_desks))
    db_desks = db.query(models.Desk).filter(models.Desk.id.not_in(db_booked_desks)).all()
    return db_desks


def create_table(db: Session, desk: schemas.Desk):
    db_desk = models.Desk(
        capacity=desk.capacity,
        price_per_hour=desk.price_per_hour,
    )
    db.add(db_desk)
    db.commit()
    db.refresh(db_desk)
    return db_desk


def get_order_by_id(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_desk_by_booker_id(db: Session, booker_id: int):
    db_order = db.query(models.Order).filter(models.Order.booker_id == booker_id).first()
    if db_order:
        return db.query(models.Desk).filter(models.Desk.id == db_order.desk_id).first()
    return None


def get_order_by_booker_id(db: Session, booker_id: int):
    db_order = db.query(models.Order).filter(models.Order.booker_id == booker_id).first()
    return db_order


def book_desk(db: Session, desk_id: int, user_id: int, booking_time: str, duration_of_booking: int):
    db_order = models.Order(
        booker_id=user_id,
        desk_id=desk_id,
        booking_time=booking_time,
        duration_of_booking=duration_of_booking
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def cancel_booking(db: Session, user_id: int):
    db_order = db.query(models.Order).filter(models.Order.booker_id == user_id).delete()
    db.commit()


def check_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    db_order.checked = True
    db.commit()
    db.refresh(db_order)
    return db_order


def get_orders(db: Session):
    db_orders = db.query(models.Order).all()
    return db_orders
