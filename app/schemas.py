from pydantic import BaseModel
from datetime import datetime

class NoteCreate(BaseModel):
    text: str  # Пайдаланушыдан келетін мәлімет

class NoteOut(BaseModel):
    id: int
    text: str
    created_at: datetime

    class Config:
        orm_mode = True  # SQLAlchemy моделін оқуға мүмкіндік береді
