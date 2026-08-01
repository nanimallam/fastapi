from sqlalchemy import Column,Integer,String,Float
from database import Base

class Mobile(Base):
    __tablename__="mobiles"

    id=Column(Integer,primary_key=True,index=True)
    brand=Column(String(100),nullable=False)
    model=Column(String(100),nullable=False)
    price=Column(Float,nullable=False)
    color=Column(String(50),nullable=False)