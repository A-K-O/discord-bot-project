from pydantic import BaseModel
from typing import Optional

# pydantic model for player information
class PlayerBase(BaseModel):
    id: int
    full_name: str
    first_name: str
    last_name: str
    is_active: bool 

