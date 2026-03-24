from datetime import datetime, timezone
from typing import Any


class NBABotError(Exception):
    """
    Base Exception Class
    """

    def __init__(self, message: str, status_code: int = 500, **kwargs):
        self.message = message
        self.status_code = status_code
        self.metadata = kwargs
        self.timestamp = datetime.now(timezone.utc).isoformat()
        super().__init__(self.message)


class PlayerNotFound(NBABotError):
    def __init__(self, player_id: int):
        super().__init__(
            message=f"Player {player_id} could not be found.",
            status_code=404,
            player_id=player_id,
            service="player_service",
        )
