# import os
# import pytest
# from sqlalchemy.ext.asyncio import (
#     create_async_engine,
#     async_sessionmaker,
#     AsyncSession,
# )
# from app.db.base import Base
# from app.core.constants import BASE_DIR

# TEST_DB_PATH = BASE_DIR / "tests" / "test.db"
# TEST_DB_URL = f"sqlite+aiosqlite:///{TEST_DB_PATH}"


# @pytest.fixture(scope="session")
# async def engine():
#     if os.path.exists(TEST_DB_PATH):
#         os.remove(TEST_DB_PATH)

#     engine = create_async_engine(
#         TEST_DB_URL,
#         echo=False,
#     )

#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

#     yield engine

#     await engine.dispose()

#     if os.path.exists(TEST_DB_PATH):
#         os.remove(TEST_DB_PATH)


# @pytest.fixture
# async def session(engine) -> AsyncSession: # type: ignore
#     SessionLocal = async_sessionmaker(
#         bind=engine,
#         expire_on_commit=False,
#         class_=AsyncSession,
#     )

#     async with SessionLocal() as session:
#         try:
#             yield session # type: ignore
#         finally:
#             await session.rollback()

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.base import Base

@pytest.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        yield s
    await engine.dispose()
