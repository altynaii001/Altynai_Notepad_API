from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class Note(Base):
    __tablename__ = 'notes'  # кесте аты PostgreSQL ішінде

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
