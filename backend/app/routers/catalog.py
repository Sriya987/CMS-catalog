from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from sqlalchemy.sql import exists
from app.dependencies import get_db
from app.models import Program, Term, Lesson

router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.get("/programs")
def catalog_programs(
    limit: int = Query(10, le=50),
    cursor: str | None = None,
    db: Session = Depends(get_db),
):
    subq = (
        db.query(Lesson.id)
        .join(Term)
        .filter(
            Term.program_id == Program.id,
            Lesson.status == "published",
        )
        .exists()
    )

    query = (
        db.query(Program)
        .filter(
            Program.status == "published",
            subq,
        )
        .order_by(desc(Program.published_at))
    )

    if cursor:
        query = query.filter(Program.published_at < cursor)

    programs = query.limit(limit).all()

    return {
        "items": [
            {
                "id": str(p.id),
                "title": p.title,
                "language_primary": p.language_primary,
                "published_at": p.published_at,
            }
            for p in programs
        ],
        "next_cursor": programs[-1].published_at if programs else None,
    }

@router.get("/programs/{id}")
def catalog_program(
    id: str,
    db: Session = Depends(get_db),
):
    program = (
        db.query(Program)
        .filter(Program.id == id, Program.status == "published")
        .first()
    )

    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    terms = (
    db.query(Term)
    .join(Lesson)
    .filter(
        Term.program_id == program.id,
        Lesson.status == "published"
    )
    .distinct()
    .order_by(Term.term_number)
    .all()
)


    return {
        "id": str(program.id),
        "title": program.title,
        "description": program.description,
        "language_primary": program.language_primary,
        "languages_available": program.languages_available,
        "terms": [
            {
                "id": str(term.id),
                "term_number": term.term_number,
                "lessons": [
                    {
                        "id": str(lesson.id),
                        "lesson_number": lesson.lesson_number,
                        "title": lesson.title,
                        "is_paid": lesson.is_paid,
                    }
                    for lesson in db.query(Lesson)
                    .filter(
                        Lesson.term_id == term.id,
                        Lesson.status == "published",
                    )
                    .order_by(Lesson.lesson_number)
                    .all()
                ],
            }
            for term in terms
        ],
    }

@router.get("/lessons/{id}")
def catalog_lesson(
    id: str,
    db: Session = Depends(get_db),
):
    lesson = (
        db.query(Lesson)
        .filter(Lesson.id == id, Lesson.status == "published")
        .first()
    )

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return {
        "id": str(lesson.id),
        "title": lesson.title,
        "content_type": lesson.content_type,
        "duration_ms": lesson.duration_ms,
        "content_language_primary": lesson.content_language_primary,
        "content_languages_available": lesson.content_languages_available,
        "content_urls_by_language": lesson.content_urls_by_language,
        "published_at": lesson.published_at,
    }

