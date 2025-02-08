from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class ModerationResult(Base):
    __tablename__ = "moderation_results"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    is_safe = Column(Boolean, nullable=False)
    reason = Column(String)
