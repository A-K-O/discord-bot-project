from fastapi import APIRouter, HTTPException, Query
from app.services import player_service
from app.core.enums import PlayerFilterSet
from app.schemas.player import (
    PlayerAwardResponse,
    PlayerBioResponse,
    PlayerStatlineResponse,
)
from typing import List, Optional

router = APIRouter(prefix="/players", tags=["Players"])

# endpoints

# @router.get("")
# async def get_players(status: PlayerFilterSet = Query(PlayerFilterSet.ALL)):
#     players_list = await player_service.get_players(status)
#
#     if not players_list:
#         raise HTTPException(status_code=404, detail="Could not return a list of players.")
#     return players_list
#
# @router.get("/search/{name}")
# async def get_player_by_name(name: str):
#     players_list = player_service.search_players(name)
#
#     return players_list


@router.get("/{player_id}", response_model=PlayerBioResponse)
async def get_player_profile(player_id: int):
    try:
        result = await player_service.get_player_bio(player_id)

        return result

    except (ValueError, RuntimeError) as e:
        # If the message mentions "not found" or "retrieve", 404 is fine.
        # Otherwise, 422 (Unprocessable Entity) is safer for validation errors.
        status_code = 404 if "Could not retrieve" in str(e) else 422
        raise HTTPException(status_code=status_code, detail=str(e))

    except Exception as e:
        # Log this on your terminal so you can see the traceback
        print(f"CRITICAL ERROR: {e}")
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred while processing the request.",
        )


@router.get("/{player_id}/awards", response_model=List[PlayerAwardResponse])
async def get_player_awards(player_id: int):
    try:
        result = await player_service.get_player_awards(player_id)

        return result

    except (ValueError, RuntimeError) as e:
        status_code = 404 if "Could not retrieve" in str(e) else 422
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred while processing the request.",
        )


# @router.get("/{player_id}/stats/career", response_model=PlayerStats)
# async def get_career_stats(player_id: int):
#     """
#     Fetch career totals for a specific player.
#     - **200**: Success
#     - **404**: Player ID exists but has no NBA career data
#     - **502**: NBA API is down or returned an invalid response
#     """
#     try:
#         # 1. Call the service and await the result
#         result = await player_service.get_career_stats(player_id)
#
#         # 2. Return the dict. FastAPI will automatically validate
#         # this against PlayerCareerStats before sending it out.
#         return result
#
#     except ValueError as ve:
#         # This catches "Logic" errors (e.g., Player has no stats)
#         # Translates to 404 Not Found
#         raise HTTPException(status_code=404, detail=str(ve))
#
#     except RuntimeError as re:
#         # This catches "Infrastructure" errors (e.g., NBA API Timeout)
#         # Translates to 502 Bad Gateway
#         raise HTTPException(status_code=502, detail=str(re))
#
#     except Exception as e:
#         # The ultimate safety net for unhandled bugs
#         # Translates to 500 Internal Server Error
#         raise HTTPException(
#             status_code=500,
#             detail=f"An unexpected error occurred: {str(e)}"
#         )


@router.get("/{player_id}/stats", response_model=List[PlayerStatlineResponse])
async def get_player_stats_endpoint(
    player_id: int,
    # Use Query to allow testing different sets like 'SeasonTotalsRegularSeason'
    stat_set: str = Query(default="SeasonTotalsRegularSeason"),
    season_id: Optional[str] = Query(default=None),
):
    try:
        # Call the specific test function you just wrote
        result = await player_service.get_player_stats(
            player_id=player_id, stat_set=stat_set, season_id=season_id
        )

        if not result:
            raise ValueError(f"No stats found for player {player_id} in set {stat_set}")

        return result

    except ValueError as ve:
        # Map validation or "not found" errors to 404/422
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        # Log the full error to your terminal for debugging
        print(f"Stats Error: {e}")
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


#
# @router.get("/{player_id}/stats/season/{season_id}", response_model=PlayerStats)
# async def get_season_stats(
#             player_id: int,
#             season_id: str | None
# ):
#     try:
#         result = await player_service.get_season_stats(player_id, season_id)
#
#         return result
#
#     except ValueError as ve:
#         raise HTTPException(status_code=404, detail=str(ve))
#
#     except RuntimeError as re:
#         raise HTTPException(status_code=404, detail=str(re))
#
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"an unexpected error occurred: {str(e)}"
#         )
