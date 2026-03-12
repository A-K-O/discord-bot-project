import redis
import json
from nba_api.stats.static import teams
# from nba_api.stats.endpoints import 
from app.core.config import NBA_HEADERS
# from app.core.enums import 


async def get_league_standings():
    
