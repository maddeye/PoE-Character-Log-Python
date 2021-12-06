from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from POEClogDatabase import Database
from POEClogApi.logger import Logger

app = FastAPI(title="POEClogApi")
app.add_middleware(CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = Logger()
db = Database(logger)


@app.get("/api/get-char/{character_name}")
@app.get("/api/get-char/{character_name}/{level}")
async def get_char(character_name: str, level: Optional[int] = 0):
    if level != 0:
        return db.get_char_with_level(character_name, level)

    return db.get_char(character_name)


@app.get("/api/list")
async def get_list():
    return db.get_all()


@app.get("/api/history/{character_name}")
async def get_history(character_name: str):
    return db.get_history(character_name)