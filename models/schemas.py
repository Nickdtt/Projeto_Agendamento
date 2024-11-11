from pydantic import BaseModel
from datetime import date
from datetime import time

class Usuario_Schema(BaseModel):
    
    nome_usuario: str
    email_usuario: str
    senha: str

class User_Response(BaseModel):

    nome_usuario: str
    email_usuario: str

class Login_Schema(BaseModel):

    email_usuario: str
    senha: str


class Agendamento_Schema(BaseModel):
    servico: str
    data: date
    hora: str

class Criar_Servico_Schema(BaseModel):
    nome_servico: str

class Cadastro_Admin_Schema(BaseModel):

    nome_usuario: str
    email_usuario: str
    senha: str
    categoria: str