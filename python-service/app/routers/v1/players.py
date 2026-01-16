from fastapi import APIRouter, HTTPException
from nba_api.stats.static import players

router = APIRouter(prefix="/players", tags=["Players"])

# endpoints

@router.get("/search/{full_name}")
async def search_player(full_name: str):
    matching_players = players.find_players_by_full_name(full_name)

    if not matching_players:
        raise HTTPException(status_code=404, detail="No player found with given name")

    return {
        "count": len(matching_players),
        "results": matching_players
    }
