from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas

router = APIRouter(prefix="/scores", tags=["Scores"])

@router.post("/add")
def add_score(score: schemas.ScoreCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter_by(id=score.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    subject = db.query(models.Subject).filter_by(id=score.subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    existing = (
        db.query(models.Score)
        .filter_by(student_id=score.student_id, subject_id=score.subject_id)
        .first()
    )

    if existing:
        existing.value = score.value
    else:
        new = models.Score(
            student_id=score.student_id,
            subject_id=score.subject_id,
            value=score.value
        )
        db.add(new)

    db.commit()
    return {"status": "ok"}

@router.get("/{student_id}")
def view_scores(student_id: int, db: Session = Depends(get_db)):
    scores = (
        db.query(models.Score, models.Subject)
        .join(models.Subject, models.Score.subject_id == models.Subject.id)
        .filter(models.Score.student_id == student_id)
        .all()
    )

    return [
        {"subject": subject.name, "value": score.value}
        for score, subject in scores
    ]
