import asyncio

from celery import Celery

from config import conf
from models import Product

app = Celery(
    __name__,
    broker=conf.BROKER_URL
)
app.conf.update(
    broker_connection_retry_on_startup=True
)

app.autodiscover_tasks(['tasks'], force=True)

async def async_send_email():
    for product in await Product.all():
        print(product)


@app.task
def send_email():
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(async_send_email())
