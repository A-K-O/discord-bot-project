from fastapi import APIRouter, HTTPException, Query
from app.services import player_service
from app.core.enums import PlayerFilterSet
from app.schemas.player import PlayerCommonInfo

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

@router.get("/{id}", response_model=PlayerCommonInfo)
async def get_player_info(id: int):
    player_info = player_service.get_player_common_info(id)

    return PlayerCommonInfo.model_validate(player_info["CommonPlayerInfo"][0])
