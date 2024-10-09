from pydantic import BaseModel

class Usuario_Schema(BaseModel):
    
    nome_usuario: str
    email_usuario: str
    senha: str