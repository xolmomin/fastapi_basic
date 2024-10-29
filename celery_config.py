from celery import Celery

from config import conf

app = Celery(
    __name__,
    broker=conf.BROKER_URL
)
app.conf.update(
    broker_connection_retry_on_startup=True
)

app.autodiscover_tasks(['tasks'], force=True)
