#!/usr/bin/env python
"""
Script para sincronizar o banco de dados com os modelos SQLAlchemy.
Usa create_all() para criar ou atualizar tabelas.
"""
import sys
import asyncio
from sqlalchemy import text, create_engine
from sqlalchemy.pool import StaticPool
from app.core.database import Base
import app.models.usuarios  # noqa: F401
import app.models.veiculos  # noqa: F401
import app.models.condutores  # noqa: F401
import app.models.manutencao  # noqa: F401
import app.models.multas  # noqa: F401
import app.models.chat  # noqa: F401


def sync_database():
    """Sincroniza o banco de dados com os modelos."""
    print("Sincronizando banco de dados com modelos...")
    try:
        # Usar engine síncrono para create_all (desenvolvimento com SQLite)
        sync_engine = create_engine(
            "sqlite:///./sigfrota_dev.db",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(sync_engine)
        print("✅ Banco de dados sincronizado com sucesso!")
        list_tables_sync(sync_engine)
        return True
    except Exception as e:
        print(f"❌ Erro ao sincronizar banco: {e}")
        import traceback
        traceback.print_exc()
        return False


def list_tables_sync(engine):
    """Lista as tabelas criadas no banco."""
    print("\nTabelas no banco de dados:")
    try:
        with engine.connect() as conn:
            # SQLite: consultar sqlite_master
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"))
            tables = result.fetchall()
            if tables:
                for table in tables:
                    print(f"  - {table[0]}")
            else:
                print("  (nenhuma tabela encontrada)")
    except Exception as e:
        print(f"  Erro ao listar tabelas: {e}")


if __name__ == "__main__":
    success = sync_database()
    sys.exit(0 if success else 1)
