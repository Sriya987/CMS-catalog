import os
from datetime import datetime, timedelta
from jose import jwt,JWTError

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "1440"))

def create_access_token(data:dict):
    to_encode = data.copy()
    expire=datetime.utcnow()+timedelta(minutes=JWT_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,JWT_SECRET,algorithm=JWT_ALGORITHM)

def decode_token(token:str):
    return jwt.decode(token,JWT_SECRET,algorithms=[JWT_ALGORITHM])
