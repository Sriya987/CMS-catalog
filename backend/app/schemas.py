from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from enum import Enum

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ContentType(str, Enum):
    video = "video"
    article = "article"

class LessonCreate(BaseModel):
    term_id: str
    lesson_number: int
    title: str

    content_type: ContentType
    duration_ms: Optional[int] = None
    is_paid: bool = False

    content_language_primary: str
    content_languages_available: List[str]

    content_urls_by_language: Dict[str, str]

    subtitle_languages: Optional[List[str]] = []
    subtitle_urls_by_language: Optional[Dict[str, str]] = {}

    publish_at: Optional[datetime] = None

class LessonUpdate(BaseModel):
    title: Optional[str] = None
    duration_ms: Optional[int] = None
    is_paid: Optional[bool] = None

    content_languages_available: Optional[List[str]] = None
    content_urls_by_language: Optional[Dict[str, str]] = None

    subtitle_languages: Optional[List[str]] = None
    subtitle_urls_by_language: Optional[Dict[str, str]] = None

class UserRole(str, Enum):
    admin = "admin"
    editor = "editor"
    viewer = "viewer"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole

class ProgramCreate(BaseModel):
    title: str
    description: Optional[str] = None

    language_primary: str
    languages_available: List[str]

    topic_ids: Optional[List[int]] = []

class ProgramUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    language_primary: Optional[str] = None
    languages_available: Optional[List[str]] = None

    topic_ids: Optional[List[int]] = None

class TermCreate(BaseModel):
    program_id: str
    term_number: int
    title: Optional[str] = None
