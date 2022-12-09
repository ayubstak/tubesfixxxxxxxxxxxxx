from sqlalchemy import Column, Integer, String
from database.db import Base
from pydantic import BaseModel, EmailStr, conint
from typing import Optional


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    nama = Column(String)
    password = Column(String)
    recommendation = Column(Integer)

    class Config:
        schema_extra = {
            "Contoh": {
                "email": "administrator@gmail.com",
                "nama" : "administrator",
                "password": "api123",
            }
        }


class UserSchema(BaseModel):
    email: EmailStr
    nama: str
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "Contoh": {
                "email": "administrator@gmail.com",
                "nama" : "administrator",
                "password": "api123",
            }
        }


class ShowUser(BaseModel):
    email: EmailStr
    nama: str
    recommendation: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "administrator@gmail.com",
                "nama" : "administrator",
                "recommendation":"Apple Pie"
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

class AnswerSchema(BaseModel):
    answer1: conint(gt=-1, lt=5)
    answer2: conint(gt=-1, lt=5)
    answer3: conint(gt=-1, lt=5)
    answer4: conint(gt=-1, lt=5)
    answer5: conint(gt=-1, lt=5)
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "answer1": 1,
                "answer2": 2,
                "answer3": 3,
                "answer4": 4,
                "answer5": 4
            }
        }