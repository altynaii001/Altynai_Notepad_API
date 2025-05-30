from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import SessionLocal, engine, Base
from . import schemas, crud

app = FastAPI()

# Базаны автоматты түрде жасау (бірінші рет)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Сессия генераторы
async def get_db():
    async with SessionLocal() as session:
        yield session

# Жазба қосу
@app.post("/notes", response_model=schemas.NoteOut)
async def create_note(note: schemas.NoteCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_note(db, note)

# Барлық жазбаларды шығару
@app.get("/notes", response_model=list[schemas.NoteOut])
async def read_notes(db: AsyncSession = Depends(get_db)):
    return await crud.get_notes(db)
