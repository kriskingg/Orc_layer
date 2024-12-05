from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.auth.utils import hash_password, verify_password, create_token
from app.core.database import get_db
from os import getenv
import sqlite3

auth_router = APIRouter()

# Models
class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

@auth_router.post("/register")
async def register_user(user: UserRegister, db: sqlite3.Connection = Depends(get_db)):
    """Register a new user."""
    cursor = db.cursor()
    cursor.execute("SELECT username FROM users WHERE username = ?", (user.username,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="User already exists")
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, hash_password(user.password)))
    db.commit()
    return {"message": "User registered successfully"}

@auth_router.post("/login")
async def login_user(user: UserLogin, db: sqlite3.Connection = Depends(get_db)):
    """Authenticate a user and return a JWT token."""
    cursor = db.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (user.username,))
    stored_password = cursor.fetchone()
    if not stored_password or not verify_password(user.password, stored_password[0]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_token(user.username)
    return {"access_token": token, "token_type": "Bearer"}
