import sqlite3
from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any

import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

DB_KEY = "keyToChange"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

router = APIRouter(prefix="/api/auth", tags=["auth"])  # used only if the path start with "auth"
security = HTTPBearer()


def get_db() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect("app.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


# Def BDD #
with sqlite3.connect("app.db") as conn:
    conn.execute(
        """CREATE TABLE IF NOT EXISTS users(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT UNIQUE NOT NULL,
               password_hash TEXT NOT NULL
           )"""
    )


# class for python code
class Credentials(BaseModel):
    username: str = Field(min_length=6, max_length=50)
    password: str = Field(min_length=6, max_length=70)


class UserOut(BaseModel):
    id: int
    username: str


# token to identify easier the user connected
def create_token(user_id: int) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": str(user_id), "exp": expire}, DB_KEY, algorithm=ALGORITHM)


# to not have to call a function in parameter (injector for fastAPI, but not liked by Ruff)
DB = Annotated[sqlite3.Connection, Depends(get_db)]
Creds = Annotated[HTTPAuthorizationCredentials, Depends(security)]


def get_current_user(db: DB, creds: Creds) -> sqlite3.Cursor | Any:
    try:
        payload = jwt.decode(creds.credentials, DB_KEY, algorithms=[ALGORITHM])
        user_id = int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid or expired token") from None
    user = db.execute("SELECT id, username FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


CurrentUser = Annotated[sqlite3.Row, Depends(get_current_user)]

# API CALL #


@router.post("/register", status_code=201)
def register(data: Credentials, db: DB) -> dict[str, str]:
    # encrypt password
    hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()
    try:
        # create user in db
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (data.username, hashed))
        db.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already used") from None
    return {"message": "Account created"}


@router.post("/login")
def login(data: Credentials, db: DB) -> dict[str, str]:
    # get the user in DB to check
    user = db.execute("SELECT * FROM users WHERE username= ?", (data.username,)).fetchone()
    # check
    if not user or not bcrypt.checkpw(data.password.encode(), user["password_hash"].encode()):
        raise HTTPException(status_code=401, detail="Wrong username or password") from None
    return {"access_token": create_token(user["id"]), "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def me(user: CurrentUser) -> dict[str, Any]:
    return {"id": user["id"], "username": user["username"]}
