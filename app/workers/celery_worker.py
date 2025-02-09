from celery import Celery
from sqlalchemy.orm import Session
from app.services.moderation import moderate_text  # Ensure correct import
from app.database import get_db  # Import database session

celery = Celery(
    "worker",
    broker="redis://redis_cache:6379/0",  # Use the correct Redis container name
    backend="redis://redis_cache:6379/0"
)


@celery.task
def async_moderate_text(text: str):
    """Runs text moderation as an async task."""
    db: Session = next(get_db())  # Get a DB session
    try:
        result = moderate_text(text, db)  # Pass DB session
        return result
    finally:
        db.close()  # Ensure DB session is closed
