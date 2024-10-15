from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os # Para acessar as variaveis de ambiente
from dotenv import load_dotenv #Para carregar as variáveis de ambiente

load_dotenv() #Carregamento das variáveis de ambiente

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

Base = declarative_base()