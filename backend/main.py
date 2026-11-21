from typing import Any

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth import router as auth_router

app = FastAPI()
# other routes
app.include_router(auth_router)

# CORS (to debug with call in navigator)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # default port for Vite
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/helloworld")
def hello() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/api/servers/{link}")
async def getserverinfo(link: str) -> Any:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.mcsrvstat.us/3/{link}")

    response.raise_for_status()

    return response.json()
