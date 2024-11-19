from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from database.database import get_db
from models.models_db import Agendamento, Servico, Usuario
from models.schemas import Cadastro_Admin_Schema, Criar_Servico_Schema
from security.security import get_current_user, get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession

admin_router = APIRouter()

@admin_router.get("/rota-adm", response_model= None)
async def rota_adm(current_adm = Depends(get_current_user), role: str = "adm"):

    if current_adm["role"] != role:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Credenciais inválidas")


    return {"resposta" : current_adm["email_usuario"]}

@admin_router.get("/lista-agendamentos", response_model= None)
async def lista_agendamentos_adm(current_adm = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    if current_adm["role"] != "adm":
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Credenciais inválidas")
    
    result = await db.execute(select(Agendamento))

    agendamentos = result.scalars().all()


    return agendamentos



@admin_router.post("/cadastro-adm", status_code= status.HTTP_201_CREATED)
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


@admin_router.post("/criar_servico")
async def criar_servico(nome_servico: Criar_Servico_Schema, db: AsyncSession = Depends(get_db)):

    novo_servico = Servico(
        nome = nome_servico.nome_servico
    )

    db.add(novo_servico)
    await db.commit()
    await db.refresh(novo_servico)

    return "Serviço criado com sucesso"