from contextlib import asynccontextmanager

from fastapi import FastAPI

from models import db
from routers import shop_router, auth_router


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await db.create_all()
    app_.include_router(auth_router)
    app_.include_router(shop_router)
    yield


app = FastAPI(lifespan=lifespan)
