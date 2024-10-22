from sqlalchemy import Integer, String, Column, Date, ForeignKey
from database.database import Base
from sqlalchemy.orm import relationship


class Usuario(Base): 
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key = True, autoincrement=True, index=True, unique=True)
    nome_usuario = Column(String, index=True, unique=True)
    email_usuario = Column(String, index=True)
    senha = Column(String, index=True) 
    
    agendamento = relationship("Agendamento", back_populates="usuario")


class Agendamento(Base):
    __tablename__= 'agendamentos'

    id = Column(Integer, primary_key=True, unique=True)
    servico = Column(String, index=True)
    data = Column(Date, index=True)
    hora = Column(String, index=True)
    nome_usuario = Column(ForeignKey("usuarios.nome_usuario"), nullable=False)

    usuario = relationship("Usuario", back_populates="agendamento")