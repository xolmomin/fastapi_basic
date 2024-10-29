from contextlib import asynccontextmanager

from fastapi import FastAPI

from models import db
from routers import shop_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.create_all()
    app.include_router(shop_router)
    yield


app = FastAPI(lifespan=lifespan)
