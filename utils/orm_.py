from fastapi import HTTPException
from starlette import status


async def get_object_or_404(cls, id: int):
    _obj = await getattr(cls, 'get')(getattr(cls, 'id') == id)
    if _obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"{cls.__name__} with id {id} not found")
    return _obj
