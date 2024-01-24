
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from sqlalchemy import ForeignKey, Column, String, Boolean, Float, Integer, ForeignKey, table
from datetime import datetime
#from database.connection import Base

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

    
class User(Base):
    __tablename__ = 'User'
    
    id = Column(Integer, primary_key = True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    wallet= Column(Float, default = 10.0)
    age = Column(Integer)
    
    
class Predict(Base):
    __tablename__ = 'Predict'
    
    id = Column(Integer, primary_key = True, autoincrement=True)
    user_id = Column(Integer,ForeignKey("User.id"), nullable=False)
    model_name=Column(String)
    N_Days = Column(Integer)
    Drug = Column(Integer)
    Age = Column(Integer)
    Sex = Column(Integer)
    Ascites = Column(Integer)
    Hepatomegaly = Column(Integer)
    Spiders = Column(Integer)
    Edema = Column(Integer)
    Bilirubin = Column(Float)
    Cholesterol = Column(Float)
    Albumin = Column(Float)
    Copper = Column(Float)
    Alk_Phos = Column(Float)
    SGOT = Column(Float)
    Triglycerides = Column(Float)
    Platelets = Column(Float)
    Prothrombin = Column(Float)
    Stage = Column(Integer)
    result = Column(Float)
    user=relationship('User', back_populates='predictions')
    
class Check(Base):
    __tablename__ = 'Check'
    
    id = Column(Integer, primary_key = True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    cost = Column(Integer)
    user = relationship('User', back_populates='checks')
    
User.checks = relationship('Check', order_by=Check.id, back_populates="user")
User.predictions = relationship('Predict', order_by=User.id,back_populates='user')

Base.metadata.create_all(bind=engine)