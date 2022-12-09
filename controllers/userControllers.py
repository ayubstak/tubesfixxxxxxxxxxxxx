from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models.userModels import User, UserSchema, AnswerSchema
from fastapi import HTTPException, status
from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from pydantic import EmailStr
from random import choice, choices


def sign_up(request: UserSchema, db: Session):
    user = db.query(User).filter(User.email == request.email).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email telah digunakan."
        )

    if len(request.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password paling sedikit memiliki 8 karakter."
        )

    hashed_password = HashPassword().create_hash(request.password)
    new_user = User(email=request.email, nama=request.nama,
                    password=hashed_password, recommendation="")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "Pesan": "Akun telah berhasil dibuat."
    }


def sign_in(request, db: Session):
    user = db.query(User).filter(User.email == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Akun tidak ditemukan."
        )

    if not HashPassword().verify_hash(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Gagal!!, periksa email/password kembali!")

    access_token = create_access_token(user.email)

    return {"access_token": access_token, "token_type": "bearer"}


def get_all_user(db: Session):
    return db.query(User).all()


def get_user(id: int, db: Session):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User tidak ditemukan."
        )

    return user

def generateFoodRecommendation(request: AnswerSchema, db: Session, user: str):
    updateUser = db.query(User).filter(User.email == user)

    answers = [request.answer1, request.answer2, request.answer3, request.answer4, request.answer5]

    angkaPenentu = 0
    courseRecommendation = choices(["'Appetizer'", "'Main Course'", "'Dessert'", "'Beverages'"])


    if(answers[0]) == 1:
        courseRecommendation = ["'Dessert'"]

    elif(answers[0]) == 2:
        courseRecommendation = ["'Main Course'"]

    elif(answers[0]) == 3:
        courseRecommendation = ["'Beverages'"]

    elif(answers[0]) == 4:
        courseRecommendation = ["'Appetizer'"]


    if(answers[1]) == 1:
        angkaPenentu = angkaPenentu + 1

    elif(answers[1]) == 2:
        angkaPenentu = angkaPenentu + 2

    elif(answers[1]) == 3:
        angkaPenentu = angkaPenentu + 3

    elif(answers[1]) == 4:
        angkaPenentu = angkaPenentu + 4

    
    if(answers[2]) == 1:
        angkaPenentu = angkaPenentu + 1

    elif(answers[2]) == 2:
        angkaPenentu = angkaPenentu + 2

    elif(answers[2]) == 3:
        angkaPenentu = angkaPenentu + 3

    elif(answers[2]) == 4:
        angkaPenentu = angkaPenentu + 4


    if(answers[3]) == 1:
        angkaPenentu = angkaPenentu + 1

    elif(answers[3]) == 2:
        angkaPenentu = angkaPenentu + 2

    elif(answers[3]) == 3:
        angkaPenentu = angkaPenentu + 3

    elif(answers[3]) == 4:
        angkaPenentu = angkaPenentu + 4


    if(answers[4]) == 1:
        angkaPenentu = angkaPenentu + 1

    elif(answers[4]) == 2:
        angkaPenentu = angkaPenentu + 2

    elif(answers[4]) == 3:
        angkaPenentu = angkaPenentu + 3

    elif(answers[4]) == 4:
        angkaPenentu = angkaPenentu + 4


    foodsRecommendation = db.execute("SELECT * FROM foods WHERE course=%s" % (courseRecommendation[0])).fetchall()

    if 4 <= angkaPenentu <= 7:
        foodRecommendation = foodsRecommendation[0]

    elif 8 <= angkaPenentu <= 10:
        foodRecommendation = foodsRecommendation[1]

    elif 11 <= angkaPenentu <= 13:
        foodRecommendation = foodsRecommendation[2]

    elif 14 <= angkaPenentu <= 16:
        foodRecommendation = foodsRecommendation[3]


    updateUser.update({'recommendation': foodRecommendation[1]})
    db.commit()

    return {"Your food recommendation is": foodRecommendation[1]}