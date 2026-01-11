from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from app.dependencies import require_role
from app.schemas import LessonCreate, LessonUpdate

router = APIRouter(prefix="/cms/lessons", tags=["cms-lessons"])

@router.post("/")
def create_lesson(
    data: LessonCreate,
    _: dict = Depends(require_role("admin", "editor"))
):
    if data.content_language_primary not in data.content_languages_available:
        raise HTTPException(
        status_code=400,
        detail="Primary content language must be in available languages"
    )

    if data.content_type == "video" and data.duration_ms is None:
        raise HTTPException(
            status_code=400,
            detail="duration_ms required for video lessons"
        )


@router.put("/{lesson_id}")
def update_lesson(
    lesson_id: str,
    data: LessonUpdate,
    _: dict = Depends(require_role("admin", "editor"))
):
    ...

@router.post("/{lesson_id}/publish")
def publish_now(
    lesson_id: str,
    _: dict = Depends(require_role("admin", "editor"))
):
    ...

@router.post("/{lesson_id}/schedule")
def schedule_publish(
    lesson_id: str,
    publish_at: datetime,
    _: dict = Depends(require_role("admin", "editor"))
):
    ...

@router.post("/{lesson_id}/archive")
def archive_lesson(
    lesson_id: str,
    _: dict = Depends(require_role("admin", "editor"))
):
    ...

@router.get("/{lesson_id}")
def get_lesson(
    lesson_id: str,
    _: dict = Depends(require_role("admin", "editor", "viewer"))
):
    ...
