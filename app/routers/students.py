from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models, schemas

router = APIRouter(prefix="/students", tags=["Students"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=schemas.StudentOut)
def register_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    new_student = models.Student(
        first_name=student.first_name,
        last_name=student.last_name
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@router.get("/", response_model=list[schemas.StudentOut])
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return students
