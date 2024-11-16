from jwt import encode
from pwdlib import PasswordHash
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import os
from dotenv import load_dotenv
from typing import Optional
import jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from database.database import get_db



load_dotenv()



SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
ALGORITHM = os.getenv("ALGORITHM")

pwd_context = PasswordHash.recommended()

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(tz=ZoneInfo('UTC')) + expires_delta
    else:
        expire = datetime.now(tz=ZoneInfo('UTC'))+ timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expirado")
    except jwt.InvalidTokenError:
        raise Exception("Token inválido")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):

    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Credenciais inválidas")

    try:
        payload = verify_token(token)

        email_usuario: str = payload.get("sub")
        role: str = payload.get("role")
        
        if email_usuario is None or role is None:
            raise credentials_exception
        return {"email_usuario": email_usuario, "role": role}
    except Exception:
        raise credentials_exception
    


