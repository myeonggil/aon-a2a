import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from aon_a2a.database.schema import Base

engine: AsyncEngine = create_async_engine(
    "sqlite+aiosqlite:///./test.db",  # 로컬 SQLite 파일
    # echo=True,
)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def create_tables():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()


# 실행
# if __name__ == "__main__":
#     asyncio.run(create_tables())
