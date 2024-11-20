import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.users_routes import users_router
from routes.security_routes import security_router
from routes.admin_routes import admin_router
from routes.services_routes import services_router
from database.database import lifespan

app = FastAPI(title="Projeto Agendamento", lifespan = lifespan)



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

app.include_router(security_router)
app.include_router(admin_router)
app.include_router(users_router)
app.include_router(services_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}



if __name__ == '__main__':
    uvicorn.run(app, port=8000)