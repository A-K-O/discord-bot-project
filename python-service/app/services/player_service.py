from os import stat
from pydantic import TypeAdapter, ValidationError
from typing import List, Type
from nba_api.stats.static import players
from nba_api.stats.endpoints import (
    playerawards,
    commonplayerinfo,
    playercareerstats,
    playerawards,
)
from app.core.config import NBA_HEADERS
from .cache import vache
from app.core.enums import PlayerCareerStatSet, PlayerFilterSet
from app.schemas.player import (
    PlayerAward,
    PlayerAwardResponse,
    PlayerBase,
    PlayerInfo,
    PlayerBioResponse,
    PlayerHeadlineStats,
    PlayerStatLine,
    PlayerStatlineResponse,
)


# --- Wrapper Function ---


async def fetch_nba_data(endpoint_class, **kwargs):
    try:
        return endpoint_class(**kwargs, headers=NBA_HEADERS, timeout=30)
    except Exception as e:
        raise RuntimeError(f"nba_api request failed: {e}")


# --- Static Functions ---


# async def get_players(status: PlayerFilterSet):
#     match status:
#         case PlayerFilterSet.ACTIVE:
#             player_list = players._get_active_players()
#         case PlayerFilterSet.INACTIVE:
#             player_list = players._get_inactive_players()
#         case _:
#             player_list = players._get_players()
#
#     list_adapter = TypeAdapter(List[PlayerBase])
#
#     return list_adapter.validate_python(player_list)
#
#
# async def get_player_suggestions(query: str) -> List[PlayerBase]:
#     ALL_PLAYERS = players.get_players()
#     query = query.lower()
#     match = []
#
#     for player in ALL_PLAYERS:
#         if player["full_name"].lower().startswith(query):
#             match.append(player)
#         if query in player["full_name"].lower():
#             match.append(player)
#
#     list_adapter = TypeAdapter(List[PlayerBase])
#
#     return list_adapter.validate_python(match)
#
#
# # --- Live Functions ---


async def get_player_stats(
    player_id: int, stat_set: str, season_id: str | None
) -> List[PlayerStatlineResponse]:
    key = f"player:{player_id}:{stat_set}"

    if season_id:
        key = key + f"{season_id}"
        cached_data = await vache.get_model_list(key, PlayerStatlineResponse)

    else:
        cached_data = await vache.get_model_list(key, PlayerStatlineResponse)

    if cached_data:
        return cached_data

    raw_data = await fetch_nba_data(
        playercareerstats.PlayerCareerStats, player_id=player_id
    )

    if not raw_data:
        raise ValueError(
            f"Could not retrieve player career stats for player ID {player_id}"
        )

    try:
        formatted_data = raw_data.get_normalized_dict()[stat_set]

        if season_id and stat_set not in PlayerCareerStatSet:
            target_set = (
                (i for i in formatted_data if i["SEASON_ID"] == season_id),
                [],
            )

        else:
            target_set = formatted_data

    except Exception as e:
        raise ValueError(f"Could not retrieve data for stat set {stat_set}:{e}")

    valid_list = []
    for obj in target_set:
        try:
            stat_instance = PlayerStatlineResponse(
                basic_info=PlayerBase.model_validate(obj),
                stat_info=PlayerStatLine.model_validate(obj),
            )
            valid_list.append(stat_instance)
        except Exception as e:
            print(ValueError(f"Stat obj was skipped as it could not be validated: {e}"))

    await vache.set(key, valid_list, 604800)
    return valid_list


# async def get_player_stats(
#     player_id: int, stat_set: str, season_id: str | None = None
# ) -> List[PlayerStatLine]:
#     data = await fetch_nba_data(
#         playercareerstats.PlayerCareerStats, player_id=player_id
#     )
#
#     if not data:
#         raise ValueError(f"data does not exist for player id: {player_id}")
#
#     try:
#         data_set = data.get_normalized_dict()[stat_set]
#
#         if not data_set:
#             raise ValueError(f"invalid or empty object for player ID: {player_id}")
#
#         if season_id and stat_set not in PlayerCareerStatSet:
#             target_set = next(
#                 (i for i in data_set if i["SEASON_ID"] == season_id), None
#             )
#             if target_set is None:
#                 return []
#
#         else:
#             target_set = data_set
#
#         list_adapter = TypeAdapter(List[PlayerStatLine])
#
#         return list_adapter.validate_python(target_set)
#
#     except (IndexError, ValueError) as e:
#         raise ValueError(
#             f"Structure of NBA data changed or is missing for player ID {player_id}: {e}"
#         )
#
#
async def get_player_bio(player_id: int) -> PlayerBioResponse:
    key = f"player:{player_id}:bio"

    cached_data = await vache.get_model(key, PlayerBioResponse)

    if cached_data:
        return cached_data

    raw_data = await fetch_nba_data(
        commonplayerinfo.CommonPlayerInfo, player_id=player_id
    )

    if not raw_data:
        raise ValueError(
            f"Could not retrieve common player info for player ID {player_id}"
        )

    try:
        formatted_data = raw_data.get_normalized_dict()
        general_data = formatted_data["CommonPlayerInfo"][0]
        headline_data = formatted_data["PlayerHeadlineStats"][0]
        bio_instance = PlayerBioResponse(
            basic_info=PlayerBase.model_validate(general_data),
            bio_info=PlayerInfo.model_validate(general_data),
            stat_info=PlayerHeadlineStats.model_validate(headline_data),
        )
    except Exception as e:
        raise ValueError(f"Data could not be validated: {e}.")

    await vache.set(key, bio_instance, 604800)
    return bio_instance


async def get_player_awards(player_id: int) -> List[PlayerAwardResponse]:
    key = f"player:{player_id}:awards"

    cached_data = await vache.get_model_list(key, PlayerAwardResponse)

    if cached_data:
        return cached_data

    raw_data = await fetch_nba_data(playerawards.PlayerAwards, player_id=player_id)

    if not raw_data:
        raise ValueError(
            f"Could not retrieve player awards data for player ID {player_id}"
        )

    formatted_data = raw_data.get_normalized_dict()["PlayerAwards"]
    valid_list = []

    for obj in formatted_data:
        try:
            award_instance = PlayerAwardResponse(
                basic_info=PlayerBase.model_validate(obj),
                award_info=PlayerAward.model_validate(obj),
            )
            valid_list.append(award_instance)
        except Exception as e:
            print(
                ValueError(
                    f"Award obj {obj} is skipped as it could not be validated: {e}"
                )
            )
            continue

    await vache.set(key, valid_list, 604800)
    return valid_list
