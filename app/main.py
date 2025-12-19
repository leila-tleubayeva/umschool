from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.db import Base, engine
from app.routers import students, scores, subjects
from app.seed import seed_subjects

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_subjects()

    yield

app = FastAPI(
    title="Exam Scores API",
    lifespan=lifespan
)

app.include_router(students.router)
app.include_router(scores.router)
app.include_router(subjects.router)

