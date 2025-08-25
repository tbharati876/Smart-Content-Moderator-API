# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, Any


# Request schemas
class TextModerationRequest(BaseModel):
    email: EmailStr
    text: str


class ImageModerationRequest(BaseModel):
    email: EmailStr
    image_url: Optional[str] = None
    image_base64: Optional[str] = None


# Response schemas
class ModerationResultOut(BaseModel):
    request_id: int
    classification: str
    confidence: Optional[float]
    reasoning: Optional[str]
    llm_response: Optional[Any]


class AnalyticsSummary(BaseModel):
    email: str
    total_requests: int
    unsafe_count: int
    breakdown: dict
