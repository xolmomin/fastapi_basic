from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from starlette.requests import Request

from models import db
from routers import shop_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.create_all()
    print("Project ishga tushdi")
    app.include_router(shop_router)
    yield
    print("Project toxtadi")


app = FastAPI(lifespan=lifespan)


@app.get("/files/{file_path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


@app.get("/files/media/{data}")
async def read_file(data: str):
    return {"file_path": data, "msg": "bu boshqa"}


from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: Optional[float] = None
    tax: float | None = None


@app.post('/')
async def root(item: Item):
    return item


@app.get("/hello/{name}")
async def say_hello(request: Request):
    name = request.path_params.get('name')
    return {"message": f"Hello {name}"}
