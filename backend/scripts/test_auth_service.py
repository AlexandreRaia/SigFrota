import sys, os, asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.database import AsyncSessionLocal
from app.repositories.usuarios import UsuarioRepository
from app.services.auth import AuthService

async def main():
    async with AsyncSessionLocal() as session:
        repo = UsuarioRepository(session)
        svc = AuthService(repo)
        token = await svc.login('admin', 'admin123')
        print('token:', token)

asyncio.run(main())
