#!/usr/bin/env python
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.security import hash_password
from app.models.usuarios import Usuario, Secretaria
import os

DATABASE_URL = "sqlite+aiosqlite:///sigfrota_dev.db"

async def create_admin():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Verificar se já existe admin
        from sqlalchemy import select
        stmt = select(Usuario).where(Usuario.username == "admin")
        result = await session.execute(stmt)
        admin = result.scalar_one_or_none()
        
        if admin:
            print("Admin já existe. Atualizando senha...")
            admin.hashed_password = hash_password("1234")
            await session.commit()
            print("✓ Senha atualizada para '1234'")
        else:
            print("Criando novo admin...")
            # Criar uma secretaria padrão primeiro
            stmt = select(Secretaria).limit(1)
            result = await session.execute(stmt)
            secretaria = result.scalar_one_or_none()
            
            if not secretaria:
                print("Criando secretaria padrão...")
                secretaria = Secretaria(
                    nome="Padrão",
                    sigla="PAD",
                    ativa=True
                )
                session.add(secretaria)
                await session.commit()
            
            admin = Usuario(
                username="admin",
                email="admin@example.com",
                first_name="Administrador",
                last_name="Sistema",
                hashed_password=hash_password("1234"),
                perfil="ADMIN",
                secretaria_id=secretaria.id,
                ativo=True,
                is_superuser=True
            )
            session.add(admin)
            await session.commit()
            print("✓ Usuário admin criado com sucesso!")
            print(f"  Username: admin")
            print(f"  Senha: 1234")
            print(f"  Perfil: ADMIN")

if __name__ == "__main__":
    asyncio.run(create_admin())
