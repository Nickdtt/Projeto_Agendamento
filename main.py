from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from models.schemas import Usuario_Schema, Agendamento_Schema, Criar_Servico_Schema, Cadastro_Admin_Schema, User_Response
from models.models_db import Usuario, Agendamento, Servico
from fastapi.middleware.cors import CORSMiddleware
from security.security import get_password_hash, verify_password, create_access_token, get_current_user


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


@app.get("/rota-protegida", response_model= None)
async def rota_protegida(current_user: dict = Depends(get_current_user)):
    return {"resposta" : f"{current_user["email_usuario"]}"}

@app.get("/rota-adm", response_model= None)
async def rota_adm(current_adm = Depends(get_current_user), role: str = "adm"):

    if current_adm["categoria"] != role:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Credenciais inválidas")


    return {"resposta" : f"{current_adm["email_usuario"]}"}

@app.get("/lista-agendamentos", response_model= None)
async def lista_agendamentos_adm(current_adm = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    if current_adm["categoria"] != "adm":
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Credenciais inválidas")
    
    result = await db.execute(select(Agendamento))

    agendamentos = result.scalars().all()


    return agendamentos


@app.post("/cadastro", status_code= status.HTTP_201_CREATED, response_model = User_Response)
async def cadastrar_usuario(usuario: Usuario_Schema, db: AsyncSession = Depends(get_db) ):
    novo_usuario = Usuario(
        nome_usuario = usuario.nome_usuario,
        email_usuario = usuario.email_usuario,
        senha = get_password_hash(usuario.senha))
    db.add(novo_usuario)
    await db.commit()
    await db.refresh(novo_usuario)
    return novo_usuario


@app.post("/cadastro-adm", status_code= status.HTTP_201_CREATED)
async def cadastrar_usuario(usuario: Cadastro_Admin_Schema, db: AsyncSession = Depends(get_db) ):
    novo_usuario = Usuario(
        nome_usuario = usuario.nome_usuario,
        email_usuario = usuario.email_usuario,
        senha = get_password_hash(usuario.senha),
        categoria = usuario.categoria
        )
    db.add(novo_usuario)
    await db.commit()
    await db.refresh(novo_usuario)
    return "Teste"

    
@app.post("/login", status_code= status.HTTP_202_ACCEPTED)
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



@app.post("/agendamento")
async def agendamento(agendamento: Agendamento_Schema, usuario_logado: Usuario = Depends(get_current_user), db:AsyncSession = Depends(get_db)):

    result = await db.execute(select(Usuario).where(Usuario.email_usuario == usuario_logado["email_usuario"]))
    usuario = result.scalar()

    novo_agendamento = Agendamento(
        servico = agendamento.servico,
        data = agendamento.data,
        hora = agendamento.hora,
        nome_usuario = usuario.nome_usuario
    )

    db.add(novo_agendamento)
    await db.commit()
    await db.refresh(novo_agendamento)

@app.get("/lista-agendamentos-usuario")
async def lista_agendamento_usuario(current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).where(Usuario.email_usuario == current_user["email_usuario"]).options(selectinload(Usuario.agendamento)))
    usuario = result.scalars().first()

    agendamentos_dict = [
        {
            "servico": agendamento.servico,
            "data": agendamento.data,
            "hora": agendamento.hora
        }
        for agendamento in usuario.agendamento
    ]

    return agendamentos_dict




@app.post("/criar_servico")
async def criar_servico(nome_servico: Criar_Servico_Schema, db: AsyncSession = Depends(get_db)):

    novo_servico = Servico(
        nome = nome_servico.nome_servico
    )

    db.add(novo_servico)
    await db.commit()
    await db.refresh(novo_servico)

    return "Serviço criado com sucesso"

@app.get("/lista_servicos")
async def listar_servicos(db: AsyncSession = Depends(get_db)):
    
    result = await db.execute(select(Servico))

    servicos = result.scalars().all()
    return servicos




if __name__ == '__main__':
    uvicorn.run(app, port=8000)