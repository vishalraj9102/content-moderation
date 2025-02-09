import openai
from sqlalchemy.orm import Session
from app.models import ModerationResult
from app.config import OPENAI_API_KEY, redis_client

client = openai.api_key = OPENAI_API_KEY

def moderate_text(text: str, db: Session):
    """Uses OpenAI API to check text moderation with caching."""
    cached_result = redis_client.get(text)
    if cached_result:
        return cached_result  # Return cached result if available
    
    try:
        response = client.moderations.create(
            model="omni-moderation-latest",
            input=text
        )

        results = response.results[0]
        flagged = results.flagged
        categories = results.categories
        reason = ", ".join([k for k, v in categories.items() if v]) if flagged else "Clean"

        moderation = ModerationResult(
            content_type="text",
            content=text,
            is_safe=not flagged,
            reason=reason
        )
        db.add(moderation)
        db.commit()
        db.refresh(moderation)

        redis_client.set(text, reason, ex=3600)  # Cache result for 1 hour
        
        return {
            "id": moderation.id,
            "content_type": "text",
            "content": text,
            "is_safe": not flagged,
            "reason": reason
        }
    except Exception as e:
        return {"error": str(e)}

def moderate_image(image_url: str, db: Session):
    """Uses OpenAI API to check image moderation."""
    try:
        response = client.moderations.create(
            model="omni-moderation-latest",
            input=[
                {"type": "image_url", "image_url": {"url": image_url}}
            ]
        )

        results = response.results[0]
        flagged = results.flagged
        categories = results.categories
        reason = ", ".join([k for k, v in categories.items() if v]) if flagged else "Clean"

        moderation = ModerationResult(
            content_type="image",
            content=image_url,
            is_safe=not flagged,
            reason=reason
        )
        db.add(moderation)
        db.commit()
        db.refresh(moderation)
        
        return {
            "id": moderation.id,
            "content_type": "image",
            "content": image_url,
            "is_safe": not flagged,
            "reason": reason
        }
    except Exception as e:
        return {"error": str(e)}


def get_moderation_result(id: int, db: Session):
    """Retrieve moderation result by ID."""
    result = db.query(ModerationResult).filter(ModerationResult.id == id).first()
    if result:
        return {
            "id": result.id,
            "content_type": result.content_type,
            "content": result.content,
            "is_safe": result.is_safe,
            "reason": result.reason,
            "created_at": result.created_at
        }
    return None


def get_moderation_stats(db: Session):
    """Retrieve moderation statistics."""
    total = db.query(ModerationResult).count()
    safe = db.query(ModerationResult).filter(ModerationResult.is_safe == True).count()
    unsafe = total - safe
    return {"total_moderated": total, "safe_count": safe, "unsafe_count": unsafe}
