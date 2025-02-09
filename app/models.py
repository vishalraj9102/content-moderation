from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ModerationResult(Base):
    """
    Stores moderation results for both text and images.
    """
    __tablename__ = "moderation_results"

    id = Column(Integer, primary_key=True, index=True)
    content_type = Column(String, nullable=False)  # "text" or "image"
    content = Column(String, nullable=False)  # Text content or image filename
    is_safe = Column(Boolean, nullable=False, default=True)  # Safe or unsafe
    reason = Column(String, nullable=True)  # Why it was flagged
    created_at = Column(DateTime, default=func.now())  # Timestamp

