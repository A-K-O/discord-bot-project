import redis
import json
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo, playercareerstats
from app.core.config import NBA_HEADERS
from app.core.enums import PlayerCareerStatSet, PlayerStatSet, PlayerFilterSet
from app.schemas.player import PlayerStatLine

cache = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# Wrapper Function


async def fetch_nba_data(endpoint_class, **kwargs):
    try:
        return endpoint_class(**kwargs, headers=NBA_HEADERS, timeout=30)
    except Exception as e:
        raise RuntimeError(f"nba_api request failed: {e}")


# --- Static Functions ---


async def get_players(status: PlayerFilterSet):
    match status:
        case PlayerFilterSet.ACTIVE:
            return players._get_active_players()
        case PlayerFilterSet.INACTIVE:
            return players._get_inactive_players()
        case _:
            return players._get_players()


async def get_player_suggestions(query: str):
    ALL_PLAYERS = players.get_players()
    query = query.lower()
    match = []

    for player in ALL_PLAYERS:
        if player["full_name"].lower().startswith(query):
            match.append(player)
        if query in player["full_name"].lower():
            match.append(player)

    return match


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

        else:
            target_set = data_set

        return target_set

    except (IndexError, ValueError) as e:
        raise ValueError(
            f"Structure of NBA data changed or is missing for player ID {player_id}: {e}"
        )


async def get_all_season_stats(player_id: int):
    data = None

    try:
        data = playercareerstats.PlayerCareerStats(
            player_id=player_id, headers=NBA_HEADERS, timeout=30
        )
    except Exception as e:
        raise RuntimeError(f"Error when retriving using nba_api: {e}")

    if not data or not hasattr(data, "season_totals_regular_season"):
        raise ValueError(
            f"nba_api returned an empty or invalid object for player ID {player_id}"
        )

    try:
        season_data = data.season_totals_regular_season.get_dict()

        if not season_data["data"]:
            raise ValueError(
                f"nba_api returned an empty or invalid object for player ID {player_id}"
            )

        headers = season_data["headers"]
        stats = season_data["data"]

        formatted_list = []

        for s in stats:
            formatted_list.append(dict(zip(headers, s)))

        return formatted_list

    except (IndexError, ValueError) as e:
        raise ValueError(
            f"Structure of NBA data changed or is missing for player ID {player_id}: {e}"
        )


async def get_season_stats(player_id: int, season_id: str | None):
    data = await fetch_nba_data(
        playercareerstats.PlayerCareerStats, player_id=player_id
    )

    if not data or not hasattr(data, "season_totals_regular_season"):
        raise ValueError(f"invalid attribute for this method.")

    try:
        season_data = data.get_normalized_dict()["SeasonTotalsRegularSeason"]

        if not season_data:
            raise ValueError(
                f"returned an empty or invalid object for player ID {player_id}"
            )

        if season_id:
            target_set = next(
                (i for i in season_data if i["SEASON_ID"] == season_id), None
            )

        else:
            target_set = season_data[-1]

        return target_set

    except (IndexError, KeyError) as e:
        raise ValueError(
            f"Structure of NBA data changed or is missing for player ID {player_id}: {e}"
        )


async def get_career_stats(player_id: int) -> list[PlayerStatLine]:

    data = await fetch_nba_data(
        playercareerstats.PlayerCareerStats, player_id=player_id
    )

    if not data or not hasattr(data, "career_totals_regular_season"):
        raise ValueError(
            f"nba_api returned an empty or invalid object for player ID: {player_id}"
        )

    try:
        career = data.get_normalized_dict()["CareerTotalsRegularSeason"]

        if not career["data"]:
            raise ValueError(f"player ID {player_id} exists but has no career totals")

        return career

    except (IndexError, KeyError) as e:
        raise ValueError(
            f"Structure of NBA data changed or is missing for player ID {player_id}: {e}"
        )


async def get_player_profile(player_id: int):
    data = None

    try:
        data = commonplayerinfo.CommonPlayerInfo(
            player_id=player_id, headers=NBA_HEADERS, timeout=30
        )
    except Exception as e:
        raise RuntimeError(f"Error when retriving data with nba_api: {e}")

    if not data:
        raise ValueError(f"player ID {player_id} exists but has no common player info")

    try:
        return data.get_normalized_dict()["CommonPlayerInfo"][0]

    except (IndexError, KeyError) as e:
        raise ValueError(
            f"Structure of NBA data changed or is missing for player ID {player_id}: {e}"
        )
