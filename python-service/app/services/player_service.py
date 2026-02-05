import redis
import json
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo, playercareerstats
from app.core.config import NBA_HEADERS

cache = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_all_players():
    return players._get_players()

def get_all_active_players():
    return players._get_active_players()

def get_all_inactive_players():
    return players._get_inactive_players()

def search_players(full_name: str):
    return players.find_players_by_full_name(full_name)

def get_player_common_info(id: int):
    return commonplayerinfo.CommonPlayerInfo(
        player_id=id,
        ).get_normalized_dict()
