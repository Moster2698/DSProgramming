import sqlite3
import pandas as pd
import numpy as np
import streamlit as st

conn = sqlite3.connect('database.sqlite')

def get_tables_infos()->list:
    query = """SELECT name FROM sqlite_master WHERE type='table' and name <> 'sqlite_sequence';"""
    dfs = list()
    query_result = psdsql(query)
    for table in query_result.name:
        query = f"""SELECT * FROM {table}"""
        df = psdsql(query)
        if df is not None:
            dfs.append(df)
    return dfs
def get_detailed_matches_by_season(season:str)->pd.DataFrame:
    query = f"""SELECT Match.id, 
                                        Country.name AS country_name, 
                                        League.name AS league_name, 
                                        season, 
                                        stage, 
                                        date,
                                        HT.team_long_name AS  home_team,
                                        AT.team_long_name AS away_team,
                                        home_team_goal, 
                                        away_team_goal                                        
                                FROM Match
                                JOIN Country on Country.id = Match.country_id
                                JOIN League on League.id = Match.league_id
                                LEFT JOIN Team AS HT on HT.team_api_id = Match.home_team_api_id
                                LEFT JOIN Team AS AT on AT.team_api_id = Match.away_team_api_id
                                WHERE season = '{season}'
                                ORDER by date;"""
    return psdsql(query)
@st.cache_data
def get_season_information(country:str = None )->pd.DataFrame:
    query = f"""SELECT c.name AS country_name, l.name AS league_name, season,
	count(distinct stage) AS games,count(distinct away_team.team_long_name) AS number_of_teams,
	Round(avg(home_team_goal),3) AS avg_home_team_goals, 
	Round(avg(away_team_goal),3) AS avg_away_team_goals, 
	Round(avg(home_team_goal-away_team_goal),3) AS avg_goal_dif, 
	sum(home_team_goal+away_team_goal) AS total_goals,
    ROUND(avg(home_team_goal+away_team_goal),3) AS avg_goals                               
	FROM Match m 
	JOIN Country c on c.id = m.country_id
	JOIN League l on l.id = m.league_id
	JOIN Team AS home_team on home_team.team_api_id = m.home_team_api_id
	JOIN Team AS away_team on away_team.team_api_id = m.away_team_api_id"""
    if country is not None and len(country) > 0:
        query += f" WHERE c.name = '{country}'"
    query += """
	GROUP BY c.name, l.name, season
	ORDER BY c.name, l.name, season DESC
    """
    goal_data =  psdsql(query)
    if goal_data is None:
        return None
    df = pd.DataFrame(index=np.sort(goal_data['season'].unique()), columns=goal_data['country_name'].unique())
    for country in goal_data.country_name.unique():
        df.loc[:, country] = list(goal_data.loc[goal_data['country_name']==country,'avg_goals'])
    return df

def psdsql(query:str):
    try:
        return pd.read_sql(query, conn)
    except:
        return None