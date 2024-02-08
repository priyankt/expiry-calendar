from sqlalchemy import Column, Integer, String, DateTime, Text, Date
from datetime import datetime
from src.lib.database import Base


class Holiday(Base):
    __tablename__ = "holidays"

    id = Column(Integer(), primary_key=True)
    date = Column(Date, nullable=False, unique=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
