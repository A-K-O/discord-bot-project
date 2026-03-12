from pydantic import BaseModel, Field, computed_field
from typing import Optional

# pydantic model for player information
class PlayerProfile(BaseModel):
    id: int = Field(alias="PERSON_ID", serialization_alias="id")
    first_name: str = Field(alias="FIRST_NAME", serialization_alias="firstName")
    last_name: str = Field(alias="LAST_NAME", serialization_alias="lastName")
    birthdate: str = Field(alias="BIRTHDATE", serialization_alias="birthDate")
    country: str = Field(alias="COUNTRY", serialization_alias="country")
    height: str = Field(alias="HEIGHT", serialization_alias="height")
    weight: str = Field(alias="WEIGHT", serialization_alias="weight")
    seasons_played: int = Field(alias="SEASON_EXP", serialization_alias="seasonsPlayed")
    position: str = Field(alias="POSITION", serialization_alias="position")
    draft_year: str = Field(alias="DRAFT_YEAR", serialization_alias="draftYear")
    draft_round: str = Field(alias="DRAFT_ROUND", serialization_alias="draftRound")
    draft_number: str = Field(alias="DRAFT_NUMBER", serialization_alias="draftNumber")

class PlayerStats(BaseModel):
    season_id: str | None= Field(default = None,alias="SEASON_ID", serialization_alias="seasonID")
    team_id: int = Field(alias="TEAM_ID", serialization_alias="teamID")
    player_age: float | None = Field(alias="PLAYER_AGE", serialization_alias="playerAge")
    games_played: int = Field(alias="GP", serialization_alias="gp")
    games_started: int = Field(alias="GS", serialization_alias="gs")
    minutes: int = Field(alias="MIN", serialization_alias="min")
    fgm: int = Field(alias="FGM", serialization_alias="fgm")
    fga: int = Field(alias="FGA", serialization_alias="fga")
    fg_pct: float = Field(alias="FG_PCT", serialization_alias="fgPercentage")
    fg3m: int = Field(alias="FG3M", serialization_alias="fg3m")
    fg3a: int = Field(alias="FG3A", serialization_alias="fg3a")
    fg3_pct: float = Field(alias="FG3_PCT", serialization_alias="fg3Percentage")
    ftm: int = Field(alias="FTM", serialization_alias="ftm")
    fta: int = Field(alias="FTA", serialization_alias="fta")
    ft_pct: float = Field(alias="FT_PCT", serialization_alias="ftPercentage")
    oreb: int = Field(alias="OREB", serialization_alias="oreb")
    dreb: int = Field(alias="DREB", serialization_alias="dreb")
    reb: int = Field(alias="REB", serialization_alias="reb")
    ast: int = Field(alias="AST", serialization_alias="ast")
    stl: int = Field(alias="STL", serialization_alias="stl")
    blk: int = Field(alias="BLK", serialization_alias="blk")
    tov: int = Field(alias="TOV", serialization_alias="tov")
    pf: int = Field(alias="PF", serialization_alias="pf")
    pts: int = Field(alias="PTS", serialization_alias="pts")

    @computed_field
    @property
    def ppg(self) -> float:
        return round(self.pts / self.games_played, 1)

    @computed_field
    @property
    def rpg(self) -> float:
       return round(self.reb / self.games_played, 1) 

    @computed_field
    @property
    def apg(self) -> float:
        return round(self.ast / self.games_played, 1)
