from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas

# Жаңа жазба қосу
async def create_note(db: AsyncSession, note: schemas.NoteCreate):
    new_note = models.Note(text=note.text)
    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    return new_note

# Барлық жазбаларды шығару
async def get_notes(db: AsyncSession):
    result = await db.execute(select(models.Note))
    return result.scalars().all()
