from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import TextModerationRequest, ImageModerationRequest, ModerationResponse
from app.services.moderation import get_moderation_result, get_moderation_stats, moderate_text, moderate_image
from app.database import get_db

router = APIRouter()

@router.post("/api/v1/moderate/text", response_model=ModerationResponse)
def moderate_text_api(request: TextModerationRequest, db: Session = Depends(get_db)):
    return moderate_text(request.text, db)

@router.post("/api/v1/moderate/image", response_model=ModerationResponse)
def moderate_image_api(request: ImageModerationRequest, db: Session = Depends(get_db)):
    return moderate_image(request.image_url, db)

@router.get("/api/v1/moderation/{id}", response_model=ModerationResponse)
def get_moderation_by_id(id: int, db: Session = Depends(get_db)):
    result = get_moderation_result(id, db)
    if not result:
        return {"error": "Moderation result not found"}
    return result


@router.get("/api/v1/stats")
def get_stats(db: Session = Depends(get_db)):
    return get_moderation_stats(db)
