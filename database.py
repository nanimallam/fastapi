import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://avnadmin:YOUR_PASSWORD@mysql-fastapi-rahulmallam1432-a239.k.aivencloud.com:13434/defaultdb"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {}
    }
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()