from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine, Base, SessionLocal
from schemas import Usuario_Schema
from models import Usuario
from fastapi.middleware.cors import CORSMiddleware
from security.security import get_password_hash, verify_password, verify_token, create_access_token


app = FastAPI(title="Projeto Agendamento")

origins = [
    "http://localhost:5173",
    "http://localhost:5173/cadastro",
    "localhost:5173/cadastro"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):

    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Credenciais inválidas")


    try:
        payload = verify_token(token)
        email_usuario: str = payload.get("sub")

        if email_usuario is None:
            raise credentials_exception
        usuario_select = await db.execute(select(Usuario).where(Usuario.email_usuario == email_usuario))
        usuario = usuario_select.scalar()
        if usuario is None:
            raise credentials_exception
        return usuario
    except Exception:
        raise credentials_exception
    




@app.get("/rota-protegida", response_model= None)
async def rota_protegida(current_user = Depends(get_current_user)):
    return {"resposta" : f"{current_user.nome_usuario}"}

@app.post("/cadastro", status_code= status.HTTP_201_CREATED)
async def cadastrar_usuario(usuario: Usuario_Schema, db: AsyncSession = Depends(get_db) ):
    novo_usuario = Usuario(
        nome_usuario = usuario.nome_usuario,
        email_usuario = usuario.email_usuario,
        senha = get_password_hash(usuario.senha))
    db.add(novo_usuario)
    await db.commit()
    await db.refresh(novo_usuario)
    return "Teste"
    
@app.post("/login", status_code= status.HTTP_202_ACCEPTED)
async def login_usuario(email_usuario: str, senha: str, db: AsyncSession = Depends(get_db)):
    usuario_select =  await db.execute(select(Usuario).where(Usuario.email_usuario == email_usuario))
    usuario = usuario_select.scalar()


    if not usuario or not verify_password(senha, usuario.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario ou senha inválida",
            headers={"WWW-Authenticate": "bearer"}
        )
    
    access_token = create_access_token(data={"sub": usuario.email_usuario})

    return {"access_token": access_token, "token_type": "bearer"}














if __name__ == '__main__':
    uvicorn.run(app, port=8000)