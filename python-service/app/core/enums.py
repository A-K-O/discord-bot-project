from enum import Enum


class PlayerFilterSet(str, Enum):
    ALL = "all"
    ACTIVE = "active"
    INACTIVE = "inactive"


class PlayerSeasonStatSet(str, Enum):
    SEASON_RANKINGS_POST = "SeasonRankingsPostSeason"
    SEASON_RANKINGS_REGULAR = "SeasonRankingsRegularSeason"
    SEASON_TOTALS_ALLSTAR = "SeasonTotalsAllStarSeason"
    SEASON_TOTALS_COLLEGE = "SeasonTotalsCollegeSeason"
    SEASON_TOTALS_POST = "SeasonTotalsPostSeason"
    SEASON_TOTALS_REGULAR = "SeasonTotalsRegularSeason"


class PlayerCareerStatSet(str, Enum):
    CAREER_TOTALS_ALLSTAR = "CareerTotalsAllStarSeason"
    CAREER_TOTALS_COLLEGE = "CareerTotalsCollegeSeason"
    CAREER_TOTALS_POST = "CareerTotalsPostSeason"
    CAREER_TOTALS_REGULAR = "CareerTotalsRegularSeason"
