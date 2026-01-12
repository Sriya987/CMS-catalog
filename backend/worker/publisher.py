import time
from datetime import datetime, timezone
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Lesson

POLL_INTERVAL_SECONDS = 60

def wait_for_db():
    for _ in range(30):
        try:
            db = SessionLocal()
            db.execute(text("SELECT 1 FROM lessons LIMIT 1"))
            db.close()
            return
        except Exception:
            print("Waiting for migrations...")
            time.sleep(2)
    raise RuntimeError("Migrations not ready")


def publish_scheduled_lessons():
    db: Session = SessionLocal()
    try:
        now = datetime.now(timezone.utc)

        lessons = (
            db.query(Lesson)
            .filter(
                Lesson.status == "scheduled",
                Lesson.publish_at <= now,
            )
            .with_for_update(skip_locked=True)
            .all()
        )

        for lesson in lessons:
            lesson.status = "published"
            lesson.published_at = now

            program = lesson.term.program
            if program.status != "published":
                program.status = "published"
                if program.published_at is None:
                    program.published_at = now

        db.commit()

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def main():
    wait_for_db()

    while True:
        try:
            publish_scheduled_lessons()
        except Exception as e:
            print("Worker error:", e)

        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
