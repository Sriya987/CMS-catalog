from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import User
from app.schemas import UserCreate
from app.security import hash_password
from app.dependencies import require_role

router = APIRouter(prefix="/cms/users", tags=["cms-users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_user(
    data: UserCreate,
    _: dict = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(400, "Email already exists")

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        role=data.role.value
    )

    db.add(user)
    db.commit()
    return {"id": str(user.id), "email": user.email, "role": user.role}


@router.get("/")
def list_users(
    _: dict = Depends(require_role("admin"))
):
    ...
