from sqlalchemy.orm import Session
from models.questionModels import QuestionSchema, Question, QuestionUpdate
from fastapi import HTTPException, status


def create_quesiton(request: QuestionSchema, db: Session, user:str):
    if (user != "administrator@gmail.com"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Fitur hanya digunakan oleh administrator."
        )

    question = db.query(Question).filter(Question.question  == request.question)

    if question.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Pertanyaan telah dibuat sebelumnya."
        )

    question_baru = Question(question=request.question, answer=request.answer)
    db.add(question_baru)
    db.commit()
    db.refresh(question_baru)

    return {
        "Pesan": "Pertanyaan berhasil dibuat."
    }


def get_questions(db: Session):
    return db.query(Question).all()


def get_question(id: int, db: Session):
    question = db.query(Question).filter(Question.questionID == id)

    if not question.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Pertanyaan tidak ada."
        )

    return question.first()


def update_question(id: int, request: QuestionUpdate, db: Session, user:str):
    if (user != "admin@gmail.com"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Fitur hanya digunakan oleh administrator."
        )

    question = db.query(Question).filter(Question.questionID == id)

    if not question.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pertanyaan tidak ada."
        )

    question.update({'question': request.question})
    db.commit()

    return {
        "Pesan": "Pertanyaan berhasil diperbarui."
    }


def delete_question(id: int, db: Session, user:str):
    if (user != "admin@gmail.com"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Fitur hanya digunakan oleh administrator."
        )

    question = db.query(Question).filter(Question.questionID == id)

    if not question.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pertanyaan tidak ada."
        )

    question.delete(synchronize_session=False)
    db.commit()

    return {
        "Pesan": "Pertanyaan berhasil dihapus."
    }