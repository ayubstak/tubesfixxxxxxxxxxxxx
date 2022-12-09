from sqlalchemy import Column, Integer, String
from database.db import Base
from pydantic import BaseModel


class Question(Base):
    __tablename__ = 'questions'

    questionID = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    answer = Column(String)

    class Config:
        schema_extra = {
            "Contoh": {
                "question": "Warna yang paling anda sukai?",
                "answer": "1. Biru  2. Hijau  3. Hitam  4. Jingga"
            }
        }


class QuestionSchema(BaseModel):
    question: str
    answer: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "question": "Warna yang paling anda sukai?",
                "answer": "1. Biru  2. Hijau  3. Hitam  4. Jingga"
            }
        }


class QuestionShow(BaseModel):
    questionID: int
    question: str
    answer: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "questionID": 3,
                "question": "Warna yang paling anda sukai?",
                "answer": "1. Biru  2. Hijau  3. Hitam  4. Jingga"
            }
        }


class QuestionUpdate(BaseModel):
    question: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "question": "Warna yang paling anda sukai?",
            }
        }