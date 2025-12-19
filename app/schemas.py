from pydantic import BaseModel

class StudentCreate(BaseModel):
    first_name: str
    last_name: str

class StudentOut(BaseModel):
    id: int
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

class ScoreCreate(BaseModel):
    student_id: int
    subject_id: int
    value: int

class ScoreOut(BaseModel):
    subject: str
    value: int

    class Config:
        from_attributes = True

class SubjectCreate(BaseModel):
    name: str

class SubjectOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True