import sqlite3
from datetime import UTC, datetime, timedelta

import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Annotated

DB_KEY = "keyToChange"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

router = APIRouter(prefix="/api/auth", tags=["auth"]) #used only if the path start with "auth"
security = HTTPBearer()

def get_db():
    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()



# Def BDD #
with sqlite3.connect("app.db") as conn:
    conn.execute(
        '''CREATE TABLE IF NOT EXISTS users(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT UNIQUE NOT NULL,
               password_hash TEXT NOT NULL
           )'''
    )

#def for python code
class Credentials(BaseModel):
    username: str = Field(min_length=6, max_length=50)
    password : str = Field(min_length=6, max_length=70)

#token to identify easier the user connected
def create_token(user_id : int) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": str(user_id), "exp": expire}, DB_KEY, algorithm = ALGORITHM)



# API CALL #

#to not have to call a function in parameter (injector for fastAPI, but not liked by Ruff)
DB = Annotated[sqlite3.Connection, Depends(get_db)]



@router.post("/register", status_code=201)
def register(data: Credentials, db : DB):
    #encrypt password
    hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()
    try:
        #create user in db
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (data.username, hashed))
        db.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already used") from None
    return {"message": "Account created"}

@router.post("/login")
def login(data: Credentials, db : DB):
    #get the user in DB to check
    user= db.execute("SELECT * FROM users WHERE username= ?", (data.username,)).fetchone()
    #check
    if not user or not bcrypt.checkpw(data.password.encode(), user["password_hash"].encode()):
        raise HTTPException(status_code=401, detail="Wrong username or password") from None
    return {"access_token" : create_token(user["id"]), "token_type":"bearer"}


