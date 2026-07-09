from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import create_tables
from app.exceptions.handlers import register_exception_handlers

# Importar todos os modelos para registrá-los no metadata antes do create_all
import app.models.usuarios  # noqa: F401
import app.models.veiculos  # noqa: F401
import app.models.condutores  # noqa: F401
import app.models.manutencao  # noqa: F401
import app.models.multas  # noqa: F401
import app.models.chat  # noqa: F401

limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup — cria tabelas no banco se não existirem
    await create_tables()
    yield
    # Shutdown


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url="/api/docs" if settings.DEBUG else None,
        redoc_url="/api/redoc" if settings.DEBUG else None,
        openapi_url="/api/openapi.json" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # Rate limiting
    application.state.limiter = limiter
    application.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception handlers
    register_exception_handlers(application)

    # API routes
    application.include_router(api_router, prefix="/api/v1")

    # Servir arquivos de mídia (sempre, inclusive em produção)
    import os
    os.makedirs(settings.MEDIA_DIR, exist_ok=True)
    application.mount("/media", StaticFiles(directory=settings.MEDIA_DIR), name="media")

    # Redireciona raiz para a documentação
    @application.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/api/docs")

    return application


app = create_application()
