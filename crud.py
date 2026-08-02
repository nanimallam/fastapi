from sqlalchemy.orm import Session
from fastapi import HTTPException, status

import models
import schemas

from auth import (
    hash_password,
    verify_password,
    create_access_token
)


# ================= MOBILE CRUD =================

def create_mobile(db: Session, mobile: schemas.MobileCreate):
    db_mobile = models.Mobile(**mobile.model_dump())

    db.add(db_mobile)
    db.commit()
    db.refresh(db_mobile)

    return db_mobile


def get_mobiles(db: Session):
    return db.query(models.Mobile).all()


def get_mobile(db: Session, mobile_id: int):
    return db.query(models.Mobile).filter(
        models.Mobile.id == mobile_id
    ).first()


def update_mobile(
    db: Session,
    mobile_id: int,
    mobile: schemas.MobileCreate
):

    db_mobile = get_mobile(db, mobile_id)

    if not db_mobile:
        return None

    db_mobile.brand = mobile.brand
    db_mobile.model = mobile.model
    db_mobile.price = mobile.price
    db_mobile.color = mobile.color

    db.commit()
    db.refresh(db_mobile)

    return db_mobile


def delete_mobile(db: Session, mobile_id: int):

    db_mobile = get_mobile(db, mobile_id)

    if not db_mobile:
        return None

    db.delete(db_mobile)
    db.commit()

    return db_mobile


def get_mobile_by_brand(db: Session, brand: str):

    return db.query(models.Mobile).filter(
        models.Mobile.brand == brand
    ).all()


# ================= USER REGISTER =================

def create_user(db: Session, user: schemas.UserCreate):

    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        is_active=True,
        is_admin=user.is_admin
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# ================= USER LOGIN =================

def login_user(db: Session, user: schemas.UserLogin):

    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Email"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Password"
        )

    access_token = create_access_token(
        {
            "sub": db_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ================= BUY MOBILE =================

def buy_mobile(
    db: Session,
    current_user,
    order: schemas.OrderCreate
):

    mobile = db.query(models.Mobile).filter(
        models.Mobile.id == order.mobile_id
    ).first()

    if mobile is None:
        raise HTTPException(
            status_code=404,
            detail="Mobile not found"
        )

    total = mobile.price * order.quantity

    db_order = models.Order(
        user_id=current_user.id,
        mobile_id=mobile.id,
        quantity=order.quantity,
        total_price=total
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order


# ================= MY ORDERS =================

def get_my_orders(
    db: Session,
    current_user
):

    return db.query(models.Order).filter(
        models.Order.user_id == current_user.id
    ).all()


# ================= ADMIN - ALL ORDERS =================

def get_all_orders(db: Session):

    return db.query(models.Order).all()