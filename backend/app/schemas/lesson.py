from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID

class LessonCreate(BaseModel):
    term_id: UUID
    lesson_number: int
    title: str
    content_type: str  # video | article
    publish_at: Optional[datetime] = None

class LessonUpdate(BaseModel):
    title: Optional[str] = None
    publish_at: Optional[datetime] = None
    status: Optional[str] = None

class LessonOut(BaseModel):
    id: UUID
    lesson_number: int
    title: str
    content_type: str
    status: str
    publish_at: Optional[datetime]
