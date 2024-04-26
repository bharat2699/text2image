import os
from celery import Celery
from text2image import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "text2image.settings")
app = Celery("text2image")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(worker_heartbeat=120, task_concurrency=4, worker_prefetch_multiplier=1)

print(app)


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
