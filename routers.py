from fastapi import APIRouter

shop_router = APIRouter()


@shop_router.get('/products')
async def get_products():
    return {}
