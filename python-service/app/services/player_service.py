import redis
import json
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo, playercareerstats
from app.core.config import NBA_HEADERS
from app.core.enums import PlayerStatSet, PlayerFilterSet

cache = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

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
        if player['full_name'].lower().startswith(query):
            match.append(player)
        if query in player['full_name'].lower():
            match.append(player)
    
    return match

# --- Live Functions ---

async def get_all_season_stats(player_id: int):
    data = None

    try:
        data = playercareerstats.PlayerCareerStats(
            player_id=player_id,
            headers=NBA_HEADERS,
            timeout=30
        )
    except Exception as e:
        raise RuntimeError(f'Error when retriving using nba_api: {e}')

    if not data or not hasattr(data, 'season_totals_regular_season'):
        raise ValueError(f'nba_api returned an empty or invalid object for player ID {player_id}')

    try:
        season_data = data.season_totals_regular_season.get_dict()

        if not season_data['data']:
            raise ValueError(f'nba_api returned an empty or invalid object for player ID {player_id}')

        headers = season_data['headers']
        stats = season_data['data']

        formatted_list = []

        for s in stats:
            formatted_list.append(dict(zip(headers,s)))

        return formatted_list

    except (IndexError, ValueError) as e:
        raise ValueError(f'Structure of NBA data changed or is missing for player ID {player_id}: {e}')

async def get_season_stats(player_id: int, season_id: str | None):
    data = None
    
    try: 
        data = playercareerstats.PlayerCareerStats(
            player_id=player_id,
            headers=NBA_HEADERS,
            timeout=30
        )        
    except Exception as e:
        raise RuntimeError(f'Error when retriving using nba_api: {e}')

    if not data or not hasattr(data, 'season_totals_regular_season'):
       raise ValueError(f'nba_api returned an empty or invalid object for player ID {player_id}') 

    try:
        season = data.season_totals_regular_season.get_dict()

        if not season['data']:
            raise ValueError(f'player ID {player_id} exists but has no career totals') 

        headers =  season['headers']
        stats = season['data']
        
        if season_id:
            target_set = next(
                (i for i in stats if i[1] == season_id),
                None
            )

        else:
            target_set = stats[-1]

        if not target_set:
            raise IndexError(f'Could not retrieve season list for player ID {player_id} and season_id {season_id}')
            
        return dict(zip(headers, target_set))
    
    except (IndexError, KeyError) as e:
        raise ValueError(f'Structure of NBA data changed or is missing for player ID {player_id}: {e}')

async def get_career_stats(player_id):
    data = None
    
    try:
         data = playercareerstats.PlayerCareerStats(
            player_id=player_id,
            headers=NBA_HEADERS,
            timeout=30
        )
    except Exception as e:
        raise RuntimeError(f'Error when retriving using nba_api: {e}')

    if not data or not hasattr(data, 'career_totals_regular_season'):
        raise ValueError(f'nba_api returned an empty or invalid object for player ID: {player_id}')

    try:
        career = data.career_totals_regular_season.get_dict() 

        if not career['data']:
            raise ValueError(f'player ID {player_id} exists but has no career totals')

        headers = career['headers']
        stats = career['data'][0]
        return dict(zip(headers, stats))

    except (IndexError, KeyError) as e:
        raise ValueError(f'Structure of NBA data changed or is missing for player ID {player_id}: {e}')


async def get_player_profile(player_id: int):
    data = None

    try:
        data = commonplayerinfo.CommonPlayerInfo(
            player_id=player_id,
            headers=NBA_HEADERS,
            timeout=30
        )
    except Exception as e:
        raise RuntimeError(f'Error when retriving data with nba_api: {e}')

    if not data:
        raise ValueError(f'player ID {player_id} exists but has no common player info')

    try:
        return data.get_normalized_dict()["CommonPlayerInfo"][0]

    except (IndexError, KeyError) as e:
        raise ValueError(f'Structure of NBA data changed or is missing for player ID {player_id}: {e}')
