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
    return db.query(models.Desk).filter(models.Desk.booker_id == None).all()


def create_table(db: Session, table: schemas.Table):
    db_table = models.Desk(
        capacity=table.capacity,
        price_per_hour=table.price_per_hour,
        booker_id=table.booker_id
    )
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table


def get_booked_tables_by_checksum(db: Session, checksum: int):
    return db.query(models.Desk).filter(models.Desk.checksum == checksum).all()


def get_booked_tables_by_booker_id(db: Session, booker_id: int):
    return db.query(models.Desk).filter(models.Desk.booker_id == booker_id).all()


def book_table(db: Session, table_id: int, user_id: int, checksum: int):
    db_table = db.query(models.Desk).filter(models.Desk.id == table_id).first()
    db_table.booker_id = user_id
    db_table.checksum = checksum
    db.commit()
    db.refresh(db_table)
    return db_table


def cancel_booking(db: Session, user_id: int):
    db_tables = db.query(models.Desk).filter(models.Desk.booker_id == user_id).all()
    for db_table in db_tables:
        db_table.booker_id = None
        db_table.checksum = None
    db.commit()
    db.refresh(db_table)
    return db_table
