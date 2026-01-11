from fastapi import APIRouter, Depends
from app.dependencies import require_role

router = APIRouter(prefix="/catalog", tags=["catalog"])

@router.get("/programs")
def catalog_programs():
    ...

@router.get("/programs/{id}")
def catalog_program():
    ...

@router.get("/lessons/{id}")
def catalog_lesson():
    ...
