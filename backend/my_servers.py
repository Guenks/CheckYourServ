import sqlite3
from typing import Annotated, Any, Literal
from urllib.parse import quote

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from auth import DB, CurrentUser

router = APIRouter(prefix="/api/my-servers", tags=["my-servers"])

# External API link to mcserverstatus
API_BASE = "https://api.mcsrvstat.us"

# mcserverstatus ask for a descriptive User-Agent for API Call
HEADERS = {"User-Agent": "CheckYourServ"}


# Create table
with sqlite3.connect("app.db") as conn:
    conn.execute(
        """CREATE TABLE IF NOT EXISTS servers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id),
            address TEXT NOT NULL,
            name TEXT NOT NULL,
            edition TEXT NOT NULL CHECK (edition IN ('java', 'bedrock')),
            UNIQUE(user_id,address,edition),
            )"""
    )


# Class for servers


# when added to DB
class ServerIn(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    # IP or DNS -> No "?" or "/" to not alter with the API call to mcserverstatus
    address: Annotated[str, Field(min_length=1, max_length=253, pattern=r"^[A-Za-z0-9.:\-\[\]]+$")]
    edition: Literal["java", "bedrock"] = "java"


# when retrieved from DB
class ServerOut(BaseModel):
    id: int
    address: str
    name: str
    edition: Literal["java", "bedrock"]


def fetch_status(address: str, edition: str) -> dict[str, Any]:
    """Get server status with an address and its edition"""
    # get final URL
    if edition == "bedrock":
        prefix = "/bedrock/3"
    else:
        prefix = "/3"
    url = f"{API_BASE}{prefix}/{quote(address, safe=':')}"

    try:
        with httpx.Client(timeout=10, headers=HEADERS) as client:
            res = client.get(url)
            res.raise_for_status()  # get error if their one
            data: dict[str, Any] = res.json()
    except (httpx.HTTPError, ValueError):
        raise HTTPException(status_code=502, detail="Status API unreachable") from None

    return data


# API CALL #


# get all user's servers
@router.get("")
def list_servers(user: CurrentUser, db: DB) -> list[ServerOut]:
    rows = db.execute(
        "SELECT id, name, address, edition FROM servers WHERE user_id = ? ORDER BY id",
        (user["id"],),
    ).fetchall()
    return [ServerOut(**dict(r)) for r in rows]


# add a user's server
@router.post("", status_code=201)
def add_server(data: ServerIn, user: CurrentUser, db: DB) -> ServerOut:
    try:
        rq = db.execute(
            "INSERT INTO servers (user_id, name, address, edition) VALUES (?,?,?,?)",
            (user["id"], data.name, data.address, data.edition),
        )
        db.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Server already saved") from None
    return ServerOut(id=rq.lastrowid, **data.model_dump())


# delete a server from a user list
@router.delete("/{server_id}", status_code=204)
def delete_server(server_id: int, user: CurrentUser, db: DB) -> None:
    # No try needed because trying to delete a no existent row don't throw an error
    rq = db.execute(
        "DELETE FROM servers WHERE id = ? AND user_id = ?",
        (server_id, user["id"]),
    )
    db.commit()
    if rq.rowcount == 0:
        raise HTTPException(status_code=404, detail="Server not found")


# get server status
@router.get("/{server_id}/status")
def server_status(server_id: int, user: CurrentUser, db: DB) -> dict[str, Any]:
    row = db.execute(
        "SELECT address, edition FROM servers WHERE id = ? AND user_id = ?",
        (server_id, user["id"]),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Server not found")
    return fetch_status(row["address"], row["edition"])
