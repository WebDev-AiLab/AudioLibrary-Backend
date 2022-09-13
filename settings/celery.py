from celery.schedules import crontab

CELERY_BROKER_URL = f"redis://redis:6379"
CELERY_RESULT_BACKEND = f"redis://redis:6379"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


# tasks
CELERY_BEAT_SCHEDULE = {
    "discover_unprocessed_tracks": {
        "task": "tracks.tasks.discover_unprocessed_tracks",
        "schedule": crontab(minute="*/1")
    }
}