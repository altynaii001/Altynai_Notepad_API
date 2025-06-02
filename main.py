from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select, Session
from database import init_db, get_session
from models import User
from schemas import UserCreate
from auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    require_role
)
from datetime import timedelta

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

# ✅ Тіркеу эндпоинті
@app.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = get_password_hash(user.password)
    
    # 🔥 Рөлді көрсету: "user" әдепкі
    new_user = User(
        username=user.username,
        password=hashed_password,
        role="user"
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username, "role": new_user.role}

# ✅ Логин + Токен
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

# ✅ Қорғалған эндпоинт – /users/me
@app.get("/users/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "username": current_user.username, "role": current_user.role}

# ✅ Тек "admin" көре алатын эндпоинт – /admin/users
@app.get("/admin/users")
def get_all_users(
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role("admin"))
):
    users = session.exec(select(User)).all()
    return users
