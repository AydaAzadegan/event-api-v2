from services.database import engine, Base
from models.event import EventModel  
from models.event import NotificationLog  
import asyncio

async def init_models():
    print("Connecting to DB and creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created (if not existed).")

if __name__ == "__main__":
    asyncio.run(init_models())
