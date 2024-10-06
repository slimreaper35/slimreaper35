import tasks
from celery_app import app

argv = ["worker", "--loglevel", "info"]
app.worker_main(argv)
