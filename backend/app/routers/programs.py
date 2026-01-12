from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Program
from app.schemas import ProgramCreate, ProgramUpdate
from app.dependencies import require_role,get_db

router = APIRouter(prefix="/cms/programs", tags=["cms-programs"])


@router.post("/")
def create_program(
    data: ProgramCreate,
    _: dict = Depends(require_role("admin", "editor")),
    db: Session = Depends(get_db),
):
    if data.language_primary not in data.languages_available:
        raise HTTPException(
            status_code=400,
            detail="Primary language must be included in available languages",
        )

    program = Program(
        title=data.title,
        description=data.description,
        language_primary=data.language_primary,
        languages_available=data.languages_available,
        status="draft",
    )

    db.add(program)
    db.commit()
    db.refresh(program)

    return {
        "id": str(program.id),
        "title": program.title,
        "status": program.status,
    }

@router.put("/{program_id}")
def update_program(
    program_id: str,
    data: ProgramUpdate,
    _: dict = Depends(require_role("admin", "editor")),
    db: Session = Depends(get_db),
):
    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    update_data = data.model_dump(exclude_unset=True)

    if "language_primary" in update_data or "languages_available" in update_data:
        primary = update_data.get("language_primary", program.language_primary)
        available = update_data.get("languages_available", program.languages_available)

        if primary not in available:
            raise HTTPException(
                status_code=400,
                detail="Primary language must be included in available languages",
            )

    for field, value in update_data.items():
        setattr(program, field, value)

    db.commit()
    db.refresh(program)

    return {
        "id": str(program.id),
        "title": program.title,
        "status": program.status,
    }


@router.post("/{program_id}/archive")
def archive_program(
    program_id: str,
    _: dict = Depends(require_role("admin", "editor")),
    db: Session = Depends(get_db),
):
    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    program.status = "archived"
    db.commit()

    return {"status": "archived"}

@router.get("/")
def list_programs(
    _: dict = Depends(require_role("admin", "editor", "viewer")),
    db: Session = Depends(get_db),
):
    programs = db.query(Program).all()

    return [
        {
            "id": str(p.id),
            "title": p.title,
            "status": p.status,
            "language_primary": p.language_primary,
        }
        for p in programs
    ]

@router.get("/{program_id}")
def get_program(
    program_id: str,
    _: dict = Depends(require_role("admin", "editor", "viewer")),
    db: Session = Depends(get_db),
):
    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    return {
        "id": str(program.id),
        "title": program.title,
        "description": program.description,
        "status": program.status,
        "language_primary": program.language_primary,
        "languages_available": program.languages_available,
        "published_at": program.published_at,
    }
