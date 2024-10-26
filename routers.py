import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import APIRouter, Query, BackgroundTasks
from sqlalchemy import func
from sqlalchemy.future import select
from starlette.requests import Request

from models import Product

shop_router = APIRouter()


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


SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', 1111))
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')


def send_email_smtp(recipient_email: str, subject: str, message: str):
    msg = MIMEMultipart()
    msg["From"] = SMTP_USERNAME
    msg["To"] = recipient_email
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, recipient_email, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")


@shop_router.get("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email_smtp, email, "Notification", "Hello")
    return {"message": "Notification sent in the background"}


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


'''
Product.objects.all()

Product.objects.get(id=2)
Product.objects.get(name='name')

Product.get(Product.id==2)
Product.get(Product.slug=='name')

'''