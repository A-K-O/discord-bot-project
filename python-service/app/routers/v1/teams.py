from fastapi import APIRouter, HTTPException, Query
from app.services import team_service
# from app.core.enums import 
# from app.schemas.team
from typing import Optional

router = APIRouter(prefix="/teams", tags=[Teams])


