import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal, create_tables
from app.models.veiculos import Marca, Modelo, TipoVeiculo


DEFAULT_TIPOS = ["CARRO", "MOTO", "CAMINHAO", "ONIBUS"]

DEFAULT_MARCAS_MODELOS = {
    "Fiat": ["Uno", "Palio", "Strada", "Doblo"],
    "Chevrolet": ["Onix", "Prisma", "S10", "Spin"],
    "Volkswagen": ["Gol", "Voyage", "Saveiro", "Fox"],
}


async def seed():
    # ensure tables exist
    await create_tables()

    async with AsyncSessionLocal() as session:  # type: AsyncSession
        # check tipos
        res = await session.execute(TipoVeiculo.__table__.select().limit(1))
        exists = res.first() is not None
        if not exists:
            print("Seeding tipos_veiculo...")
            for nome in DEFAULT_TIPOS:
                t = TipoVeiculo(nome=nome, ativo=True)
                session.add(t)
            await session.commit()

        # check marcas
        res = await session.execute(Marca.__table__.select().limit(1))
        exists = res.first() is not None
        if not exists:
            print("Seeding marcas and modelos...")
            for marca_nome, modelos in DEFAULT_MARCAS_MODELOS.items():
                m = Marca(nome=marca_nome, ativo=True)
                session.add(m)
                await session.flush()  # get id
                for modelo_nome in modelos:
                    mo = Modelo(marca_id=m.id, nome=modelo_nome, ativo=True)
                    session.add(mo)
            await session.commit()

    print("Seeding complete")


if __name__ == "__main__":
    asyncio.run(seed())
