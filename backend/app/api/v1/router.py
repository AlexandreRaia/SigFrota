from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    chat,
    condutores,
    manutencao,
    multas,
    parametrizacoes,
    usuarios,
    veiculos,
)

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(usuarios.router)
api_router.include_router(veiculos.router)
api_router.include_router(parametrizacoes.router)
api_router.include_router(condutores.router)
api_router.include_router(manutencao.router)
api_router.include_router(multas.router)
api_router.include_router(chat.router)
