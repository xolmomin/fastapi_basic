import asyncio

from celery import shared_task

from models import Product


async def async_send_email():
    for product in await Product.all():
        print(product)


@shared_task
def send_email():
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(async_send_email())
