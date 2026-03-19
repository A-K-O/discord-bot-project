from pydantic import BaseModel, Field, computed_field


class PlayerBase(BaseModel):
    player_id: int = Field(alias="player_id", serialization_alias="playerId")
    full_name: str = Field(alias="full_name", serialization_alias="fullName")
    first_name: str = Field(alias="first_name", serialization_alias="firstName")
    last_name: str = Field(alias="last_name", serialization_alias="lastName")
    is_active: bool = Field(alias="is_active", serialization_alias="isActive")


class PlayerInfo(BaseModel):
    birthdate: str = Field(alias="BIRTHDATE", serialization_alias="birthDate")
    last_affiliation: str = Field(
        alias="LAST_AFFILIATION", serialization_alias="lastAffiliation"
    )
    country: str = Field(alias="COUNTRY", serialization_alias="country")
    height: str = Field(alias="HEIGHT", serialization_alias="height")
    weight: str = Field(alias="WEIGHT", serialization_alias="weight")
    draft_year: str = Field(alias="DRAFT_YEAR", serialization_alias="draftYear")
    draft_round: str = Field(alias="DRAFT_ROUND", serialization_alias="draftRound")
    draft_number: str = Field(alias="DRAFT_NUMBER", serialization_alias="draftNumber")
    experience: int = Field(alias="SEASON_EXP", serialization_alias="experience")
    jersey_number: str = Field(alias="JERSEY", serialization_alias="jerseyNumber")
    position: str = Field(alias="POSITION", serialization_alias="position")
    team_id: int = Field(alias="TEAM_ID", serialization_alias="teamId")
    team_city: str = Field(alias="TEAM_CITY", serialization_alias="teamCity")
    team_name: str = Field(alias="TEAM_NAME", serialization_alias="teamName")
    dl_flag: str = Field(alias="DLEAGUE_FLAG", serialization_alias="dlFlag")
    nba_flag: str = Field(alias="NBA_FLAG", serialization_alias="nbaFlag")
    gp_flag: str = Field(alias="GAMES_PLAYED_FLAG", serialization_alias="gpFlag")


class PlayerHeadlineStats(BaseModel):
    player_id: int = Field(alias="PLAYER_ID", serialization_alias="playerId")
    player_name: str = Field(alias="PLAYER_NAME", serialization_alias="playerName")
    time_frame: str = Field(alias="TimeFrame", serialization_alias="timeFrame")
    pts: float = Field(alias="PTS", serialization_alias="pts")
    ast: float = Field(alias="AST", serialization_alias="ast")
    reb: float = Field(alias="REB", serialization_alias="reb")
    pie: float = Field(alias="PIE", serialization_alias="pie")


class PlayerStatLine(BaseModel):
    games_played: int = Field(alias="GP", serialization_alias="gamesPlayed")
    games_started: int = Field(alias="GS", serialization_alias="gamesStarted")
    minutes: int = Field(alias="MIN", serialization_alias="minutes")
    fgm: int = Field(alias="FGM", serialization_alias="fgm")
    fga: int = Field(alias="FGA", serialization_alias="fga")
    fgp: float = Field(alias="FG_PCT", serialization_alias="fgp")
    ftm: int = Field(alias="FTM", serialization_alias="ftm")
    fta: int = Field(alias="FTA", serialization_alias="fta")
    ftp: int = Field(alias="FT_PCT", serialization_alias="ftp")
    fg3m: int = Field(alias="FG3M", serialization_alias="fg3m")
    fg3a: int = Field(alias="FG3A", serialization_alias="fg3a")
    fg3p: float = Field(alias="FG3_PCT", serialization_alias="fg3p")
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


class PlayerGameLog(PlayerStatLine):
    season_id: str = Field(alias="SEASON_ID", serialization_alias="seasonId")
    game_id: str = Field(alias="GAME_ID", serialization_alias="gameId")
    game_date: str = Field(alias="GAME_DATE", serialization_alias="gameDate")
    matchup: str = Field(alias="MATCHUP", serialization_alias="matchup")
    wl: str = Field(alias="WL", serialization_alias="wl")
    plus_minus: int = Field(alias="PLUS_MINUS", serialization_alias="plusMinus")
    video_available: int = Field(
        alias="VIDEO_AVAILABLE", serialization_alias="videoAvailable"
    )


class PlayerAward(BaseModel):
    player_info: PlayerBase
    team: str = Field(alias="TEAM", serialization_alias="team")
    description: str = Field(alias="DESCRIPTION", serialization_alias="description")
    anba_team_number: str = Field(
        alias="ALL_NBA_TEAM_NUMBER", serialization_alias="allNBATeamNumber"
    )
    season: str = Field(alias="SEASON", serialization_alias="season")
    month: str = Field(alias="MONTH", serialization_alias="month")
    week: str = Field(alias="week", serialization_alias="week")
    conference: str = Field(alias="CONFERENCE", serialization_alias="conference")
    award_type: str = Field(alias="TYPE", serialization_alias="awardType")
    subtype1: str = Field(alias="SUBTYPE1", serialization_alias="subtype1")
    subtype2: str = Field(alias="SUBTYPE2", serialization_alias="subtype2")
    subtype3: str = Field(alias="SUBTYPE3", serialization_alias="subtype3")


# Response Models


class PlayerBioResponse(BaseModel):
    basic_info: PlayerBase
    bio_info: PlayerInfo
    stat_info: PlayerHeadlineStats


class PlayerStatlineResponse(BaseModel):
    basic_info: PlayerBase
    stat_info: PlayerStatLine
