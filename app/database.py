from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# .env файлын жүктеу
load_dotenv()

# .env ішінен база сілтемесін оқу
DATABASE_URL = os.getenv("DATABASE_URL")

# Асинхронды қозғалтқыш жасау
engine = create_async_engine(DATABASE_URL, echo=True)

# Сессия жасау
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Базалық класс (модельдер үшін)
Base = declarative_base()
