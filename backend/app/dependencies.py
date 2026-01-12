from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError,ExpiredSignatureError
from app.auth import decode_token
from app.db import SessionLocal
from sqlalchemy.orm import Session

security = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    try:
        payload = decode_token(token)
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

def require_role(*roles):
    def checker(
        credentials: HTTPAuthorizationCredentials = Depends(security),
    ):
        if credentials is None:
            raise HTTPException(status_code=401, detail="Not authenticated")

        token = credentials.credentials
        payload = decode_token(token)

        if payload["role"] not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")

        return payload

    return checker



def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
