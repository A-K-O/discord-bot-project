from fastapi import FastAPI
from nba_service.api.players import router as players_router

app = FastAPI(
    title="NBA Stats Microservice",
    version="1.0.0"
)

app.include_router(players_router, prefix="/players")

@app.get("/health")
def health_check():
    return {"status": "ok"}
