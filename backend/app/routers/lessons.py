from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.db import SessionLocal
from app.dependencies import require_role
from app.models import Lesson, Term, Program
from app.schemas import LessonCreate, LessonUpdate

router = APIRouter(prefix="/cms/lessons", tags=["cms-lessons"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_lesson(
    data: LessonCreate,
    _: dict = Depends(require_role("admin", "editor")),
    db: Session = Depends(get_db),
):
    if data.content_language_primary not in data.content_languages_available:
        raise HTTPException(
            status_code=400,
            detail="Primary content language must be in available languages",
        )

    if data.content_type == "video" and data.duration_ms is None:
        raise HTTPException(
            status_code=400,
            detail="duration_ms required for video lessons",
        )

    # Ensure term exists
    term = db.query(Term).filter(Term.id == data.term_id).first()
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")

    lesson = Lesson(
        term_id=data.term_id,
        lesson_number=data.lesson_number,
        title=data.title,
        content_type=data.content_type,
        duration_ms=data.duration_ms,
        is_paid=data.is_paid,
        content_language_primary=data.content_language_primary,
        content_languages_available=data.content_languages_available,
        content_urls_by_language=data.content_urls_by_language,
        status="scheduled" if data.publish_at else "draft",
        publish_at=data.publish_at,
    )

    db.add(lesson)
    db.commit()
    db.refresh(lesson)

    return {
        "id": str(lesson.id),
        "status": lesson.status,
        "publish_at": lesson.publish_at,
    }


@router.put("/{lesson_id}")
def update_lesson(
    lesson_id: str,
    data: LessonUpdate,
    _: dict = Depends(require_role("admin", "editor")),
    db: Session = Depends(get_db),
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    # --- Apply updates if provided ---
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(lesson, field, value)

    # --- Validations ---
    if lesson.content_language_primary not in lesson.content_languages_available:
        raise HTTPException(
            status_code=400,
            detail="Primary content language must be in available languages",
        )

    if lesson.content_type == "video" and lesson.duration_ms is None:
        raise HTTPException(
            status_code=400,
            detail="duration_ms required for video lessons",
        )

    # Scheduled lessons must have publish_at
    if lesson.status == "scheduled" and lesson.publish_at is None:
        raise HTTPException(
            status_code=400,
            detail="publish_at required for scheduled lessons",
        )

    db.commit()
    db.refresh(lesson)

    return {
        "id": str(lesson.id),
        "title": lesson.title,
        "status": lesson.status,
        "publish_at": lesson.publish_at,
    }


@router.post("/{lesson_id}/publish")
def publish_now(
    lesson_id: str,
    _: dict = Depends(require_role("admin", "editor")),
    db: Session = Depends(get_db),
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    lesson.status = "published"
    lesson.published_at = datetime.now(timezone.utc)

    db.commit()

    # Program auto-publish rule
    program = (
        db.query(Program)
        .join(Term)
        .filter(Term.id == lesson.term_id)
        .first()
    )

    if program and program.status != "published":
        program.status = "published"
        program.published_at = lesson.published_at
        db.commit()

    return {"status": "published"}

@router.post("/{lesson_id}/schedule")
def schedule_publish(
    lesson_id: str,
    publish_at: datetime,
    _: dict = Depends(require_role("admin", "editor")),
    db: Session = Depends(get_db),
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    lesson.status = "scheduled"
    lesson.publish_at = publish_at

    db.commit()

    return {"status": "scheduled", "publish_at": publish_at}


@router.post("/{lesson_id}/archive")
def archive_lesson(
    lesson_id: str,
    _: dict = Depends(require_role("admin", "editor")),
    db: Session = Depends(get_db),
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    lesson.status = "archived"
    db.commit()

    return {"status": "archived"}


@router.get("/{lesson_id}")
def get_lesson(
    lesson_id: str,
    _: dict = Depends(require_role("admin", "editor", "viewer")),
    db: Session = Depends(get_db),
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return {
        "id": str(lesson.id),
        "title": lesson.title,
        "status": lesson.status,
        "publish_at": lesson.publish_at,
        "published_at": lesson.published_at,
    }
