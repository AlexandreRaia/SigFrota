import sys
import os
import asyncio

# garante que o diretório pai ('backend') esteja no sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.database import AsyncSessionLocal
from app.repositories.usuarios import UsuarioRepository

async def main():
    async with AsyncSessionLocal() as session:
        repo = UsuarioRepository(session)
        user = await repo.get_by_username('admin')
        print('user:', user)
        if user:
            print('username:', user.username)
            print('hashed:', user.hashed_password)

asyncio.run(main())
