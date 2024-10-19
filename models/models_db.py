from sqlalchemy import Integer, String, Column
from database.database import Base


class Usuario(Base): 
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key = True, autoincrement=True, index=True, unique=True)
    nome_usuario = Column(String, index=True)
    email_usuario = Column(String, index=True)
    senha = Column(String, index=True) 