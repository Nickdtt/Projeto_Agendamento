from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database.database import get_db
from models.models_db import Agendamento, Usuario
from models.schemas import Agendamento_Schema, User_Response, Usuario_Schema
from security.security import get_current_user, get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession


users_router = APIRouter()


@users_router.post("/cadastro", status_code= status.HTTP_201_CREATED, response_model = User_Response)
async def cadastrar_usuario(usuario: Usuario_Schema, db: AsyncSession = Depends(get_db) ):
    novo_usuario = Usuario(
        nome_usuario = usuario.nome_usuario,
        email_usuario = usuario.email_usuario,
        senha = get_password_hash(usuario.senha))
    db.add(novo_usuario)
    await db.commit()
    await db.refresh(novo_usuario)
    return novo_usuario


@users_router.post("/agendamento")
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

@users_router.get("/lista-agendamentos-usuario")
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

@users_router.get("/rota-protegida", response_model= None)
async def rota_protegida(current_user: dict = Depends(get_current_user)):
    return {"resposta" : f"{current_user["email_usuario"]}"}