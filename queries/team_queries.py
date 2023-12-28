import functions as f
import pandas as pd
import typing
def get_teams_attributes() -> pd.DataFrame:
    query = """Select * from team_attributes;"""
    return f.psdsql(query)

def get_teams_by_points() -> pd.DataFrame:
    query = """Select  h.season as Season,h.name as League, t.team_long_name,Sum(3*(h.wins + a.wins) + (h.draws + a.draws)) as Pt,
        Sum(h.wins + a.wins) as V, Sum(h.draws + a.draws) as D, Sum(h.losses + a.losses) as L, (h.goals + a.goals) as Gd FROM home_stats h JOIN away_stats 
        a On h.team = a.team and h.season = a.season JOIN team t on h.team = t.team_api_id JOIN Country c on h.country = c.id 
        GROUP BY h.season, t.team_long_name,
        Order by pt desc"""
    return f.psdsql(query)
def get_most_goals_done_all_time() -> pd.DataFrame:
    query = """Select  t.team_long_name,Sum(h.goals + a.goals) as Gd FROM home_stats h JOIN away_stats 
            a On h.team = a.team and h.season = a.season JOIN team t on h.team = t.team_api_id JOIN Country c on h.country = c.id 
            GROUP BY  t.team_long_name
            Order by Gd desc
            """
    return f.psdsql(query)
def get_win_rate() -> pd.DataFrame:
    query = """Select t.team_long_name,Sum(h.wins + a.wins)  as V,Sum(h.draws + a.draws) as D,(Sum(h.wins + a.wins) + Sum(h.draws + a.draws) + Sum(h.losses + a.losses)) as P, Round(Sum(h.wins + a.wins) * 1.0 /(Sum(h.wins + a.wins) + Sum(h.draws + a.draws) + Sum(h.losses + a.losses)),3) as freq
        FROM home_stats h JOIN away_stats a On h.team = a.team and h.season = a.season JOIN team t on h.team = t.team_api_id JOIN Country c on h.country = c.id 
        GROUP BY t.team_long_name 
        Order by freq desc"""
    return f.psdsql(query)

def get_most_goals_by_season() -> pd.DataFrame:
    query = """Select h.season, t.team_long_name,Sum(h.goals + a.goals) as Gd FROM home_stats h JOIN away_stats 
            a On h.team = a.team and h.season = a.season JOIN team t on h.team = t.team_api_id JOIN Country c on h.country = c.id 
            GROUP BY  t.team_long_name,h.season
            Order by Gd desc"""
    return f.psdsql(query)

def get_most_overall() -> pd.DataFrame:
    query = """Select t.team_long_name,t.team_api_id, t.team_fifa_api_id,STRFTIME('%Y', ta.date) || "/" || (STRFTIME('%Y', ta.date) +1) as season,
(ta.buildUpPlaySpeed +
coalesce (ta.buildUpPlayDribbling,Round(avg(ta.buildUpPlayDribbling) over ()))+
ta.buildUpPlayPassing + ta.chanceCreationPassing + ta.chanceCreationCrossing + 
ta.chanceCreationShooting + ta.defencePressure+ ta.defenceAggression+ ta.defenceTeamWidth) as overall,
ta.buildUpPlaySpeed,
coalesce (ta.buildUpPlayDribbling,Round(avg(ta.buildUpPlayDribbling) over ()))  as PlayDribbling, 
ta.buildUpPlayPassing, ta.chanceCreationPassing, ta.chanceCreationCrossing, 
ta.chanceCreationShooting, ta.defencePressure, ta.defenceAggression, ta.defenceTeamWidth
from Team_Attributes ta join Team t  on ta.team_fifa_api_id  = t.team_fifa_api_id
Order by overall desc"""
    return f.psdsql(query)