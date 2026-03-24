from pydantic import TypeAdapter
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo, playercareerstats
from valkey.commands import valkeymodules
from app.core.config import NBA_HEADERS
from app.core.enums import PlayerCareerStatSet, PlayerFilterSet
from app.schemas.player import (
    PlayerBase,
    PlayerInfo,
    PlayerBioResponse,
    PlayerHeadlineStats,
    PlayerStatLine,
)


# --- Wrapper Function ---


async def fetch_nba_data(endpoint_class, **kwargs):
    try:
        return endpoint_class(**kwargs, headers=NBA_HEADERS, timeout=30)
    except Exception as e:
        raise RuntimeError(f"nba_api request failed: {e}")


# --- Cache Functions ---


async def get_cache_data(key: str):
    data = valkeymodules


async def set_cache_data(key: str, data: dict, expire: int = 3600):
    pass


# --- Static Functions ---


async def get_players(status: PlayerFilterSet):
    match status:
        case PlayerFilterSet.ACTIVE:
            player_list = players._get_active_players()
        case PlayerFilterSet.INACTIVE:
            player_list = players._get_inactive_players()
        case _:
            player_list = players._get_players()

    list_adapter = TypeAdapter(list[PlayerBase])

    return list_adapter.validate_python(player_list)


async def get_player_suggestions(query: str) -> list[PlayerBase]:
    ALL_PLAYERS = players.get_players()
    query = query.lower()
    match = []

    for player in ALL_PLAYERS:
        if player["full_name"].lower().startswith(query):
            match.append(player)
        if query in player["full_name"].lower():
            match.append(player)

    list_adapter = TypeAdapter(list[PlayerBase])

    return list_adapter.validate_python(match)


# --- Live Functions ---


async def get_player_stats(
    player_id: int, stat_set: str, season_id: str | None = None
) -> list[PlayerStatLine]:
    data = await fetch_nba_data(
        playercareerstats.PlayerCareerStats, player_id=player_id
    )

    if not data:
        raise ValueError(f"data does not exist for player id: {player_id}")

    try:
        data_set = data.get_normalized_dict()[stat_set]

        if not data_set:
            raise ValueError(f"invalid or empty object for player ID: {player_id}")

        if season_id and stat_set not in PlayerCareerStatSet:
            target_set = next(
                (i for i in data_set if i["SEASON_ID"] == season_id), None
            )
            if target_set is None:
                return []

        else:
            target_set = data_set

        list_adapter = TypeAdapter(list[PlayerStatLine])

        return list_adapter.validate_python(target_set)

    except (IndexError, ValueError) as e:
        raise ValueError(
            f"Structure of NBA data changed or is missing for player ID {player_id}: {e}"
        )


async def get_player_bio(player_id: int) -> PlayerBioResponse:
    data = await fetch_nba_data(commonplayerinfo.CommonPlayerInfo, player_id=player_id)

    if not data:
        raise ValueError(f"invalid or empty object for player ID: {player_id}")

    try:
        norm_data = data.get_normalized_dict()

        bio_data = norm_data["CommonPlayerInfo"]
        stats_data = norm_data["PlayerHeadlineStats"]

        return PlayerBioResponse(
            basic_info=PlayerBase.model_validate(bio_data),
            bio_info=PlayerInfo.model_validate(bio_data),
            stat_info=PlayerHeadlineStats.model_validate(stats_data),
        )
    except (IndexError, ValueError) as e:
        raise ValueError(
            f"Structure of NBA data has changed or is missing for player ID {player_id}: {e}"
        )
