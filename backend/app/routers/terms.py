from fastapi import APIRouter, Depends
from app.dependencies import require_role
from app.schemas import TermCreate

router = APIRouter(prefix="/cms/terms", tags=["cms-terms"])

@router.post("/")
def create_term(
    data: TermCreate,
    _: dict = Depends(require_role("admin", "editor"))
):
    ...

@router.get("/by-program/{program_id}")
def list_terms(
    program_id: str,
    _: dict = Depends(require_role("admin", "editor", "viewer"))
):
    ...
