import os

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL: str = os.getenv(key="DATABASE_URL", default="")

engine: Engine = create_engine(url=DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
