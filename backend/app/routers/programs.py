from fastapi import APIRouter, Depends
from app.dependencies import require_role
from app.schemas import ProgramCreate, ProgramUpdate

router = APIRouter(prefix="/cms/programs", tags=["cms-programs"])

@router.post("/")
def create_program(
    data: ProgramCreate,
    _: dict = Depends(require_role("admin", "editor"))
):
    ...

@router.put("/{program_id}")
def update_program(
    program_id: str,
    data: ProgramUpdate,
    _: dict = Depends(require_role("admin", "editor"))
):
    ...

@router.post("/{program_id}/archive")
def archive_program(
    program_id: str,
    _: dict = Depends(require_role("admin", "editor"))
):
    ...

@router.get("/")
def list_programs(
    _: dict = Depends(require_role("admin", "editor", "viewer"))
):
    ...

@router.get("/{program_id}")
def get_program(
    program_id: str,
    _: dict = Depends(require_role("admin", "editor", "viewer"))
):
    ...
