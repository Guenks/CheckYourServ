from typing import Annotated, Any, Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import Field

from auth import router as auth_router
from my_servers import ADDRESS_PATTERN, fetch_status
from my_servers import router as servers_router

app = FastAPI()
# other routes
app.include_router(auth_router)
app.include_router(servers_router)

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


@app.get("/api/servers/{address}")
def getserverinfo(
    address: Annotated[str, Field(min_length=1, max_length=253, pattern=ADDRESS_PATTERN)],
    edition: Literal["java", "bedrock"] = "java",
) -> Any:
    return fetch_status(address, edition)
