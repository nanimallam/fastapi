from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Mobile(Base):
    __tablename__ = "mobiles"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    color = Column(String(50), nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    orders = relationship("Order", back_populates="user")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    mobile_id = Column(Integer, ForeignKey("mobiles.id"))

    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)

    user = relationship("User", back_populates="orders")
    mobile = relationship("Mobile")