from pydantic import BaseModel, Field, computed_field
from typing import Optional

# pydantic model for player information
class PlayerCommonInfo(BaseModel):
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
