from sqlalchemy.orm import Session
import models
import schemas

def create_mobile(db:Session,mobile:schemas.MobileCreate):
    db_mobile=models.Mobile(**mobile.model_dump())

    db.add(db_mobile)
    db.commit()
    db.refresh(db_mobile)

    return db_mobile


def get_mobiles(db:Session):
    return db.query(models.Mobile).all()


def get_mobile(db:Session,mobile_id:int):
    return db.query(models.Mobile).filter(
        models.Mobile.id==mobile_id
    ).first()


def update_mobile(db:Session,mobile_id:int,mobile:schemas.MobileCreate):

    db_mobile=get_mobile(db,mobile_id)

    if not db_mobile:
        return None

    db_mobile.brand=mobile.brand
    db_mobile.model=mobile.model
    db_mobile.price=mobile.price
    db_mobile.color=mobile.color

    db.commit()
    db.refresh(db_mobile)

    return db_mobile


def delete_mobile(db:Session,mobile_id:int):

    db_mobile=get_mobile(db,mobile_id)

    if not db_mobile:
        return None

    db.delete(db_mobile)
    db.commit()

    return db_mobile


def get_mobile_by_brand(db:Session,brand:str):

    return db.query(models.Mobile).filter(
        models.Mobile.brand==brand
    ).all()