# app/seed.py
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.db import SessionLocal
from app.models import Program, Term, Lesson

def run():
    db = SessionLocal()

    # ---- PROGRAMS ----
    program1 = Program(
        id=uuid4(),
        title="Full Stack Foundations",
        description="Learn backend + frontend",
        language_primary="en",
        languages_available=["en", "hi"],
        status="published",
        published_at=datetime.now(timezone.utc),
        posters={
            "en": {
                "portrait": "https://cdn.example.com/p1/en-portrait.jpg",
                "landscape": "https://cdn.example.com/p1/en-landscape.jpg",
            },
            "hi": {
                "portrait": "https://cdn.example.com/p1/hi-portrait.jpg",
                "landscape": "https://cdn.example.com/p1/hi-landscape.jpg",
            },
        },
    )

    program2 = Program(
        id=uuid4(),
        title="Python Basics",
        description="Intro to Python",
        language_primary="en",
        languages_available=["en"],
        status="draft",
        posters={
            "en": {
                "portrait": "https://cdn.example.com/p2/en-portrait.jpg",
                "landscape": "https://cdn.example.com/p2/en-landscape.jpg",
            }
        },
    )

    db.add_all([program1, program2])
    db.commit()

    # ---- TERMS ----
    term1 = Term(
        id=uuid4(),
        program_id=program1.id,
        term_number=1,
        title="Core Concepts",
    )

    term2 = Term(
        id=uuid4(),
        program_id=program2.id,
        term_number=1,
        title="Getting Started",
    )

    db.add_all([term1, term2])
    db.commit()

    now = datetime.now(timezone.utc)

    # ---- LESSONS (6 total) ----
    lessons = [
        Lesson(
            id=uuid4(),
            term_id=term1.id,
            lesson_number=1,
            title="Intro to Web",
            content_type="video",
            duration_ms=600000,
            status="published",
            published_at=now,
            content_language_primary="en",
            content_languages_available=["en", "hi"],
            content_urls_by_language={
                "en": "https://cdn.example.com/l1/en.mp4",
                "hi": "https://cdn.example.com/l1/hi.mp4",
            },
            thumbnails={
                "en": {
                    "portrait": "https://cdn.example.com/l1/en-p.jpg",
                    "landscape": "https://cdn.example.com/l1/en-l.jpg",
                }
            },
        ),
        Lesson(
            id=uuid4(),
            term_id=term1.id,
            lesson_number=2,
            title="Frontend Basics",
            content_type="article",
            status="published",
            published_at=now,
            content_language_primary="en",
            content_languages_available=["en"],
            content_urls_by_language={
                "en": "https://cdn.example.com/l2/en.html"
            },
            thumbnails={
                "en": {
                    "portrait": "https://cdn.example.com/l2/en-p.jpg",
                    "landscape": "https://cdn.example.com/l2/en-l.jpg",
                }
            },
        ),
        Lesson(
            id=uuid4(),
            term_id=term1.id,
            lesson_number=3,
            title="Backend Basics",
            content_type="video",
            duration_ms=720000,
            status="scheduled",
            publish_at=now + timedelta(minutes=2),
            content_language_primary="en",
            content_languages_available=["en", "hi"],
            content_urls_by_language={
                "en": "https://cdn.example.com/l3/en.mp4",
                "hi": "https://cdn.example.com/l3/hi.mp4",
            },
            thumbnails={
                "en": {
                    "portrait": "https://cdn.example.com/l3/en-p.jpg",
                    "landscape": "https://cdn.example.com/l3/en-l.jpg",
                }
            },
        ),
        Lesson(
            id=uuid4(),
            term_id=term2.id,
            lesson_number=1,
            title="Python Intro",
            content_type="video",
            duration_ms=500000,
            status="published",
            published_at=now,
            content_language_primary="en",
            content_languages_available=["en"],
            content_urls_by_language={
                "en": "https://cdn.example.com/l4/en.mp4"
            },
            thumbnails={
                "en": {
                    "portrait": "https://cdn.example.com/l4/en-p.jpg",
                    "landscape": "https://cdn.example.com/l4/en-l.jpg",
                }
            },
        ),
        Lesson(
            id=uuid4(),
            term_id=term2.id,
            lesson_number=2,
            title="Variables",
            content_type="article",
            status="draft",
            content_language_primary="en",
            content_languages_available=["en"],
            content_urls_by_language={
                "en": "https://cdn.example.com/l5/en.html"
            },
            thumbnails={
                "en": {
                    "portrait": "https://cdn.example.com/l5/en-p.jpg",
                    "landscape": "https://cdn.example.com/l5/en-l.jpg",
                }
            },
        ),
        Lesson(
            id=uuid4(),
            term_id=term2.id,
            lesson_number=3,
            title="Loops",
            content_type="video",
            duration_ms=450000,
            status="draft",
            content_language_primary="en",
            content_languages_available=["en"],
            content_urls_by_language={
                "en": "https://cdn.example.com/l6/en.mp4"
            },
            thumbnails={
                "en": {
                    "portrait": "https://cdn.example.com/l6/en-p.jpg",
                    "landscape": "https://cdn.example.com/l6/en-l.jpg",
                }
            },
        ),
    ]

    db.add_all(lessons)
    db.commit()
    db.close()

    print("✅ Seed completed successfully")

if __name__ == "__main__":
    run()
