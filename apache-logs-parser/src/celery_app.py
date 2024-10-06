from celery import Celery

app = Celery(
    "tasks",
    broker="redis://redis:6379/1",
    backend="db+sqlite:///celery_backend.sqlite",
    task_track_started=True,
    broker_connection_retry_on_startup=True,
)
