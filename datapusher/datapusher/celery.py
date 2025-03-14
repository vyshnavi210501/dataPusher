import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "datapusher.settings")

app = Celery("datapusher")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from installed Django apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
