import sys
sys.path.insert(0, '/backend')

import asyncio
from app.core.database import AsyncSessionLocal
from app.models.usuarios import Usuario
from app.core.security import hash_password

async def create_test_user():
    async with AsyncSessionLocal() as session:
        # Verificar se usuário já existe
        from sqlalchemy import select
        stmt = select(Usuario).where(Usuario.username == "admin")
        result = await session.execute(stmt)
        existing = result.scalars().first()
        
        if existing:
            print(f"Usuário 'admin' já existe")
            # Atualizar senha
            existing.password_hash = hash_password("1234")
            await session.merge(existing)
        else:
            # Criar novo usuário
            user = Usuario(
                username="admin",
                email="admin@sigfrota.local",
                password_hash=hash_password("1234"),
                is_admin=True,
                is_active=True
            )
            session.add(user)
        
        await session.commit()
        print("Usuário de teste criado/atualizado: admin / 1234")

asyncio.run(create_test_user())
