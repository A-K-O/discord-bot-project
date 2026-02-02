from fastapi import APIRouter, HTTPException, Query
from app.services import player_service
from app.core.enums import PlayerFilterSet

router = APIRouter(prefix="/players", tags=["Players"])

# endpoints

@router.get("")
async def get_players(status: PlayerFilterSet = Query(PlayerFilterSet.ALL)):
    match (status):
        case PlayerFilterSet.ACTIVE:
            players_list = player_service.get_all_active_players()
        case PlayerFilterSet.INACTIVE:
            players_list = player_service.get_all_inactive_players()
        case PlayerFilterSet.ALL:
            players_list = player_service.get_all_players()

    if not players_list:
        raise HTTPException(status_code=404, detail="Could not return a list of players.")

    return {
        "count": len(players_list),
        "results": players_list
    }

@router.get("{full_name}")
async def search_player(full_name: str):
    matching_players = player_service.search_players(full_name)

    if not matching_players:
        raise HTTPException(status_code=404, detail="No player found with given name")

    return {
        "count": len(matching_players),
        "results": matching_players
    }
