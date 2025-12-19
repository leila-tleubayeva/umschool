from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Subject

SUBJECTS = [
    "Математика",
    "Русский язык",
    "Физика",
    "Химия",
    "Биология",
    "Информатика",
    "История",
    "Обществознание",
    "Английский язык",
]

def seed_subjects():
    db: Session = SessionLocal()
    try:
        existing = {
            s.name for s in db.query(Subject.name).all()
        }

        for name in SUBJECTS:
            if name not in existing:
                db.add(Subject(name=name))

        db.commit()
    finally:
        db.close()
