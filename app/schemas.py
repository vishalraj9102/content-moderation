from pydantic import BaseModel

class TextModerationRequest(BaseModel):
    text: str

class ModerationResponse(BaseModel):
    id: int
    is_safe: bool
    reason: str
