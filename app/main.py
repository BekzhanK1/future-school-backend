from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI
from app.db.init_db import init_db
from app.api.v1 import items


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


app.include_router(items.router, prefix="/v1")
