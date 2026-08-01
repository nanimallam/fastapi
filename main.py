from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session

import crud
import schemas

from database import Base,engine,SessionLocal

Base.metadata.create_all(bind=engine)

app=FastAPI()


def get_db():

    db=SessionLocal()

    try:
        yield db

    finally:
        db.close()


@app.post("/mobiles",response_model=schemas.MobileResponse)
def create(mobile:schemas.MobileCreate,
           db:Session=Depends(get_db)):

    return crud.create_mobile(db,mobile)


@app.get("/mobiles",
         response_model=list[schemas.MobileResponse])
def read_all(db:Session=Depends(get_db)):

    return crud.get_mobiles(db)


@app.get("/mobiles/{mobile_id}",
         response_model=schemas.MobileResponse)
def read_one(mobile_id:int,
             db:Session=Depends(get_db)):

    mobile=crud.get_mobile(db,mobile_id)

    if not mobile:
        raise HTTPException(404,"Mobile not found")

    return mobile


@app.put("/mobiles/{mobile_id}",
         response_model=schemas.MobileResponse)
def update(mobile_id:int,
           mobile:schemas.MobileCreate,
           db:Session=Depends(get_db)):

    updated=crud.update_mobile(db,mobile_id,mobile)

    if not updated:
        raise HTTPException(404,"Mobile not found")

    return updated


@app.delete("/mobiles/{mobile_id}")
def delete(mobile_id:int,
           db:Session=Depends(get_db)):

    deleted=crud.delete_mobile(db,mobile_id)

    if not deleted:
        raise HTTPException(404,"Mobile not found")

    return {"message":"Deleted Successfully"}


@app.get("/brand/{brand}",
         response_model=list[schemas.MobileResponse])
def get_brand(brand:str,
              db:Session=Depends(get_db)):

    return crud.get_mobile_by_brand(db,brand)

