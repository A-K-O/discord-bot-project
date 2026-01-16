from fastapi import FastAPI
from app.routers.v1 import players

app = FastAPI(
    title="NBA Stats Microservice",
    description="A microservice to get NBA player and team stats.",
    version="1.0.0"
)

# routers

app.include_router(players.router, prefix="/api/v1", tags=["Players"])

@app.get("/health", tags=["Monitoring"])
def health_check():
    """
    Health check endpoint to ensure the service is running.
    """
    return {"status": "ok"}
