from enum import Enum 

class PlayerStatSet(str, Enum):
    """Name attributed to each stat object"""
    SEASON_REGULAR = 'SeasonTotalsRegularSeason'
    CAREER_REGULAR = 'CareerTotalsRegularSeason'
    SEASON_POST = 'SeasonTotalsPostSeason'
    CAREER_POST = 'CareerTotalsPostSeason'
    SEASON_ALLSTAR = 'SeasonTotalAllStarSeason'
    CAREER_ALLSTAR = 'CareerTotalsAllStarSeason'
    SEASON_COLLEGE = 'SeasonTotalsCollegeSeason'
    CAREER_COLEGE = 'CareerTotalsCollegeSeason'
    SEASON_SHOWCASE = 'SeasonTotalsShowcaseSeason'
    CAREER_SHOWCASE = 'CareerTotalsShowcaseSeason'
    RANKINGS_REGULAR = 'SeasonRankingsRegularSeason'
    RANKINGS_POST = 'SeasonRankingsPostSeason'
    SEASON_HIGHS = 'SeasonHighs'

class PlayerFilterSet(str, Enum):
    ALL = "all"
    ACTIVE = "active"
    INACTIVE = "inactive"

