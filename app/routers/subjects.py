from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app import models

router = APIRouter(prefix="/subjects", tags=["Subjects"])

@router.get("/")
def get_subjects(db: Session = Depends(get_db)):
    subjects = db.query(models.Subject).all()
    return [{"id": s.id, "name": s.name} for s in subjects]
