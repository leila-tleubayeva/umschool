from db import SessionLocal
from models import Subject

subjects = [
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

db = SessionLocal()

for name in subjects:
    if not db.query(Subject).filter_by(name=name).first():
        db.add(Subject(name=name))

db.commit()
print("Subjects added!")
