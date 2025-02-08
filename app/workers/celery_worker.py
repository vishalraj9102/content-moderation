from celery import Celery
from app.config import REDIS_URL

celery = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)

@celery.task
def process_text_moderation(text):
    # Simulate AI moderation check
    return {"text": text, "is_safe": True, "reason": "Clean content"}
