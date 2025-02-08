from sqlalchemy.orm import Session
from app.models import ModerationResult
from app.workers.celery_worker import process_text_moderation

def moderate_text(text: str, db: Session):
    task = process_text_moderation.delay(text)
    result = task.get()
    moderation = ModerationResult(content=text, is_safe=result["is_safe"], reason=result["reason"])
    db.add(moderation)
    db.commit()
    db.refresh(moderation)
    return moderation
