from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from models.models_db import Servico


services_router = APIRouter()

@services_router.get("/lista_servicos")
async def listar_servicos(db: AsyncSession = Depends(get_db)):
    
    result = await db.execute(select(Servico))

    servicos = result.scalars().all()
    return servicos