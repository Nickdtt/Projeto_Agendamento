from sqlalchemy import Integer, String, Column, Date, ForeignKey
from database.database import Base
from sqlalchemy.orm import relationship


class Usuario(Base): 
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key = True, autoincrement=True, index=True, unique=True)
    nome_usuario = Column(String, index=True, unique=True)
    email_usuario = Column(String, index=True)
    senha = Column(String, index=True)
    categoria = Column(String, index=True, default="usuario")
    
    agendamento = relationship("Agendamento", back_populates="usuario", cascade="all, delete-orphan")

    

class Agendamento(Base):
    __tablename__= 'agendamentos'

    id = Column(Integer, primary_key=True, unique=True)
    servico = Column(String, index=True)
    data = Column(Date, index=True)
    hora = Column(String, index=True)
    nome_usuario = Column(ForeignKey("usuarios.nome_usuario"), nullable=False)

    usuario = relationship("Usuario", back_populates="agendamento")

    class Config:
        orm_mode = True


class Servico(Base):
    __tablename__= 'servicos'

    id = Column(Integer, primary_key=True, unique=True)
    nome = Column(String, index=True)

    class Config:
        orm_mode = True