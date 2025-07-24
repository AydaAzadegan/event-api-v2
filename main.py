from fastapi import FastAPI
from contextlib import asynccontextmanager
from tasks.notification_worker import check_upcoming_events
from controllers import event_controller
import asyncio
@asynccontextmanager
async def lifespan(app: FastAPI):
    import asyncio
    task = asyncio.create_task(check_upcoming_events())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)
app.include_router(event_controller.router)

