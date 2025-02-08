from fastapi import APIRouter, Depends
from app.schemas import TextModerationRequest, ModerationResponse
from app.services.moderation import moderate_text
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/api/v1/moderate/text", response_model=ModerationResponse)
def moderate_text_api(request: TextModerationRequest, db: Session = Depends(get_db)):
    result = moderate_text(request.text, db)
    return result
