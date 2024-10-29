import time

from fastapi import APIRouter, Query
from sqlalchemy import func
from sqlalchemy.future import select
from starlette.requests import Request

from models import Product
from schemas import CreateProduct, ResponseProduct
from utils.orm_ import get_object_or_404

shop_router = APIRouter()


@shop_router.get('/products/{_id}', response_model=ResponseProduct)
async def get_product(_id: int):
    return await get_object_or_404(Product, _id)


@shop_router.post('/products')
async def create_product(product: CreateProduct) -> ResponseProduct:
    return await Product.create(**product.model_dump())


@shop_router.get('/products')
async def get_products(
        name: str = Query(None, description="Name of the product to search for"),
        min_price: int = Query(None, description="Minimum price filter"),
        max_price: int = Query(None, description="Maximum price filter"),
        page: int = Query(1, ge=1, description="Page number"),
        page_size: int = Query(10, ge=1, le=100, description="Number of products per page")
):
    query = select(Product)

    if name:
        query = query.where(Product.name.ilike(f'%{name}%'))
    if min_price:
        query = query.where(Product.price >= min_price)
    if max_price:
        query = query.where(Product.price <= max_price)

    offset = (page - 1) * page_size

    query = query.offset(offset).limit(page_size)
    products = await Product.run_query(query)

    total_query = select(func.count()).select_from(Product)
    if name:
        total_query = total_query.where(Product.name.ilike(f'%{name}%'))
    if min_price:
        total_query = total_query.where(Product.price >= min_price)
    if max_price:
        total_query = total_query.where(Product.price <= max_price)

    total_count = await Product.query_count(total_query)

    return {
        "total_count": total_count,
        "page": page,
        "page_size": page_size,
        "products": products
    }


@shop_router.get("/generate", name='generate_products')
async def generate_products(request: Request):
    data = {
        'product': Product
    }

    start = time.time()

    for k, count in dict(request.query_params).items():
        if k in data:
            await data[k].generate(int(count))

    end = time.time()
    return {"message": "OK", "spend_time": int(end - start)}
