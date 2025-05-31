from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI
from app.db.init_db import init_db, init_superadmin
from app.db.session import AsyncSessionLocal
from app.api.v1 import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    async with AsyncSessionLocal() as db:
        await init_superadmin(db)

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


app.include_router(router, prefix="/v1")
