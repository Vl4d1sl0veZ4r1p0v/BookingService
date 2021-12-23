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
        number_of_persons=user.number_of_persons,
        table_id=user.table_id,
        booking_time=user.booking_time
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_free_tables(db: Session):
    return db.query(models.Table).filter(models.Table.booker_id is None).all()


def create_table(db: Session, table: schemas.Table):
    db_table = models.Table(
        capacity=table.capacity,
        price_per_place=table.price_per_place,
        booker_id=table.booker_id
    )
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table


def book_table(db: Session, table_id: int, user_id: int):
    db_table = db.query(models.Table).filter(models.Table.id == table_id).first()
    db_table.booker_id = user_id
    db.commit()
    db.refresh(db_table)
    return db_table
