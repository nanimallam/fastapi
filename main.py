from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import models

from database import Base, engine, SessionLocal
from auth import get_current_user, verify_admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mobile Store API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ================= HOME =================

@app.get("/")
def home():
    return {"message": "Welcome to Mobile Store API"}


#  AUTH 

@app.post("/register", response_model=schemas.UserResponse)
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    return crud.create_user(db, user)


@app.post("/login", response_model=schemas.Token)
def login(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    return crud.login_user(db, user)


# MOBILE 

# Logged-in users can view mobiles

@app.get("/mobiles", response_model=list[schemas.MobileResponse])
def get_all_mobiles(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_mobiles(db)


@app.get("/mobiles/{mobile_id}", response_model=schemas.MobileResponse)
def get_mobile(
    mobile_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    mobile = crud.get_mobile(db, mobile_id)

    if not mobile:
        raise HTTPException(404, "Mobile not found")

    return mobile


# Admin only

@app.post("/mobiles", response_model=schemas.MobileResponse)
def create_mobile(
    mobile: schemas.MobileCreate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(verify_admin)
):
    return crud.create_mobile(db, mobile)


@app.put("/mobiles/{mobile_id}", response_model=schemas.MobileResponse)
def update_mobile(
    mobile_id: int,
    mobile: schemas.MobileCreate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(verify_admin)
):
    updated = crud.update_mobile(db, mobile_id, mobile)

    if not updated:
        raise HTTPException(404, "Mobile not found")

    return updated


@app.delete("/mobiles/{mobile_id}")
def delete_mobile(
    mobile_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(verify_admin)
):
    deleted = crud.delete_mobile(db, mobile_id)

    if not deleted:
        raise HTTPException(404, "Mobile not found")

    return {"message": "Mobile deleted successfully"}


@app.get("/brand/{brand}", response_model=list[schemas.MobileResponse])
def get_brand(
    brand: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_mobile_by_brand(db, brand)


# ORDERS 

@app.post("/orders", response_model=schemas.OrderResponse)
def buy_mobile(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.buy_mobile(db, current_user, order)


@app.get("/my-orders", response_model=list[schemas.OrderResponse])
def my_orders(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_my_orders(db, current_user)


@app.get("/orders", response_model=list[schemas.OrderResponse])
def all_orders(
    db: Session = Depends(get_db),
    admin: models.User = Depends(verify_admin)
):
    return crud.get_all_orders(db)

