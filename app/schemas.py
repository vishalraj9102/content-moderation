from pydantic import BaseModel

class TextModerationRequest(BaseModel):
    text: str

class ImageModerationRequest(BaseModel):
    image_url: str

class ModerationResponse(BaseModel):
    id: int
    content_type: str
    content: str
    is_safe: bool
    reason: str
