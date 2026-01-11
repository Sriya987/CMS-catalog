from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import User
from app.auth import create_access_token
from app.security import verify_password

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(email:str,password:str,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==email).first()
    if not user or not verify_password(password,user.password_hash):
        raise HTTPException(status_code=401,detail="Invalid credentials")
    
    token = create_access_token({
        "sub":str(user.id),
        "role":user.role.value
    })
    return {"access_token":token}
