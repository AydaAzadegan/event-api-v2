from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import Depends

DATABASE_URL = "postgresql+asyncpg://event_user:event_pass@db/event_db"

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()

async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# FastAPI dependency
async def get_db():
    async with async_session() as session:
        yield session
