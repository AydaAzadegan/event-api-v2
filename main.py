from fastapi import FastAPI
from controllers.event_controller import router as event_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": " Your event API is running!"}

# Include event routes
app.include_router(event_router)
