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
    query = """Select team_long_name , overall from Team_stats ts Limit 10"""
    return f.psdsql(query)

def get_most_points() -> pd.DataFrame:
    query = """Select t.team_long_name,
    3*Sum(h.wins + a.wins) + Sum(h.draws + a.draws) as Points
    FROM home_stats h JOIN away_stats a On h.team = a.team and h.season = a.season JOIN team t on h.team = t.team_api_id JOIN Country c on h.country = c.id 
    GROUP BY t.team_long_name 
    Order by Points desc"""
    return f.psdsql(query)

def get_points_and_max_overall() -> pd.DataFrame:
    query = """
Select g.team_long_name,g.GD, Max(ts.overall) as overall FROM(
Select h.season, t.team_long_name,t.team_api_id, Sum(h.goals + a.goals) as Gd FROM home_stats h JOIN away_stats 
            a On h.team = a.team and h.season = a.season JOIN team t on h.team = t.team_api_id JOIN Country c on h.country = c.id 
            GROUP BY  t.team_long_name
            Order by Gd desc) g Join Team_stats ts  on g.team_api_id = ts.team_api_id
            Group by g.team_long_name
            order by g.gd desc, ts.overall desc
    """
    return f.psdsql(query)