import redis
import json
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo, playercareerstats
from app.core.config import NBA_HEADERS

cache = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_raw_player_data(id: int):
    """
    Obtain raw JSON data for a player using player id
    """
    cache_key = f'player:stats:{id}'
    
    cached_bundle = cache.get(cache_key)
    if cached_bundle is not None:
        return json.loads(str(cached_bundle))
    
    print(f"Cache miss for {id} Fetching from NBA...")
    raw_data = playercareerstats.PlayerCareerStats(
        player_id=id,
        headers=NBA_HEADERS,
        timeout=30
    ).get_dict()
    
    cache.set(cache_key, json.dumps(cached_bundle), ex=86400)


def get_all_players():
    return players._get_players()

def get_all_active_players():
    return players._get_active_players()

def get_all_inactive_players():
    return players._get_inactive_players()

def search_players(full_name: str):
    return players.find_players_by_full_name(full_name)

