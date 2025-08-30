from sqlalchemy.orm.decl_api import DeclarativeBase
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

from datetime import datetime
Base: DeclarativeBase = declarative_base()


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    access_token = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class Stock(Base):

    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    stock_code = Column(String, nullable=False, index=True, comment="Unique stock number")
    stock_name = Column(String, nullable=False, comment="Stock name")
    market_division = Column(String, nullable=False, comment="ex) KOSPI, KOSDAQ")
    created_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, nullable=False)
