import asyncio
import traceback

from app.core.database import AsyncSessionLocal, create_tables
from app.models.veiculos import Veiculo


def make_payload():
    return {
        "placa": "ABC1234",
        "chassi": "9BWZZZ377VT004251",
        "renavam": "12345678901",
        "prefixo": "P-01",
        "marca_id": 1,
        "modelo_id": 1,
        "ano_fabricacao": 2020,
        "km_atual": 1000,
    }


async def run():
    try:
        await create_tables()
        async with AsyncSessionLocal() as session:
            payload = make_payload()
            v = Veiculo(**payload)
            session.add(v)
            await session.commit()
            print('Created vehicle id=', v.id)
    except Exception as e:
        print('Exception:')
        traceback.print_exc()


if __name__ == '__main__':
    asyncio.run(run())
