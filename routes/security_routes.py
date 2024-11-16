from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from models.models_db import Usuario
from security.security import create_access_token, verify_password

security_router = APIRouter()


@security_router.post("/login", status_code= status.HTTP_202_ACCEPTED)
async def login_usuario(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    usuario_select =  await db.execute(select(Usuario).where(Usuario.email_usuario == form_data.username))
    usuario = usuario_select.scalar()


    if not usuario or not verify_password(form_data.password, usuario.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario ou senha inválida",
            headers={"WWW-Authenticate": "bearer"}
        )
    
    access_token = create_access_token(data={"sub": usuario.email_usuario, "role": usuario.categoria})

    return {"access_token": access_token, "token_type": "bearer"}