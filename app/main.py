from fastapi import FastAPI
from app.db import Base, engine
from app.routers import students, scores, subjects

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Exam Scores API")

app.include_router(students.router)
app.include_router(scores.router)
app.include_router(subjects.router)
