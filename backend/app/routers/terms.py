from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import require_role
from app.schemas import TermCreate
from app.db import SessionLocal
from app.models import Term, Program

router = APIRouter(prefix="/cms/terms", tags=["cms-terms"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_term(
    data: TermCreate,
    _: dict = Depends(require_role("admin", "editor")),
    db: Session = Depends(get_db),
):
    # ensure program exists
    program = db.query(Program).filter(Program.id == data.program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    term = Term(
        program_id=data.program_id,
        title=data.title,
        term_number=data.term_number,
        status="draft",
    )

    db.add(term)
    db.commit()
    db.refresh(term)

    return {
        "id": str(term.id),
        "program_id": str(term.program_id),
        "title": term.title,
        "term_number": term.term_number,
        "status": term.status,
    }


@router.get("/by-program/{program_id}")
def list_terms(
    program_id: str,
    _: dict = Depends(require_role("admin", "editor", "viewer")),
    db: Session = Depends(get_db),
):
    terms = (
        db.query(Term)
        .filter(Term.program_id == program_id)
        .order_by(Term.term_number)
        .all()
    )

    return [
        {
            "id": str(t.id),
            "title": t.title,
            "term_number": t.term_number,
            "status": t.status,
        }
        for t in terms
    ]
