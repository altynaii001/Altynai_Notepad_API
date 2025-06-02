from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import select, Session
from models import User
from schemas import UserCreate, UserLogin
from database import engine, get_session, init_db
from auth import get_password_hash, verify_password  # ✅

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = get_password_hash(user.password)  # ✅
    new_user = User(username=user.username, password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username}

@app.post("/login")
def login(user: UserLogin, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if not db_user or not verify_password(user.password, db_user.password):  # ✅
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful", "username": db_user.username}
