import pandas as pd
import streamlit as st
import sqlite3

st.cache_data
def __get_connection():
    return sqlite3.connect('database.sqlite')
def __psdsql(query:str):
    try:
        df = pd.read_sql_query(query, __get_connection())
        return df
    except:
        return None
    
def __create_views():
    query = """CREATE TEMP VIEW home_stats
    AS 
	SELECT name, season, home_team as team,Sum(win_games) as wins,
		Sum(draw_games) as draws, Sum(lost_games) as losses,
		Sum(goals) as goals from(
			Select l.name, m.season, m.id, m.home_team_api_id as home_team, m.home_team_goal > m.away_team_goal as win_games,
			(m.home_team_goal = m.away_team_goal) as draw_games ,
			(m.home_team_goal < m.away_team_goal) as lost_games,
			m.home_team_goal as goals
			 FROM Match m Join League l on m.league_id = l.id
			 Group by m.season, m.home_team_api_id, m.away_team_api_id
			 ) 
	group by home_team, season
 	order by name, season;""" 
    cur = __get_connection().cursor
    cur.execute(query)
    query = """CREATE  TEMP VIEW away_stats
    AS 
    Select name, season,away_team as team,Sum(win_games) as wins,
            Sum(draw_games) as draws, Sum(lost_games) as losses, Sum(goals) as goals from(
    Select l.name, m.season, m.id, m.away_team_api_id as away_team,
    (m.home_team_goal < m.away_team_goal) as win_games,
    (m.home_team_goal = m.away_team_goal) as draw_games,
    (m.home_team_goal > m.away_team_goal) as lost_games,
    m.away_team_goal as goals
    FROM Match m Join League l on m.league_id = l.id
    Group by m.season, m.home_team_api_id,m.away_team_api_id
    ) group by away_team, season
    order by name, season;"""
    cur.execute(query)

def get_table_stats_by_season_and_country(season:str, country: str):
    query = f"""Select h.season as Season,h.name as League,t.team_long_name as Team , 
    3*(h.wins + a.wins) + (h.draws + a.draws) as Pt,
    (h.wins + a.wins) as V, (h.draws + a.draws) as D, (h.losses + a.losses) as L, (h.goals + a.goals) as Gd
    FROM home_stats h 
    JOIN away_stats  a
    On h.team = a.team and h.season = a.season
    JOIN team t on h.team = t.team_api_id 
    WHERE h.season = '{season}'
    Order by h.name, h.season, pt Desc, (h.goals + a.goals) desc"""
    return __psdsql(query)
def get_leagues() -> pd.DataFrame:
    query = 'Select * from League'
    return __psdsql(query)

def get_country() -> pd.DataFrame:
    query = 'Select name from Country'
    return __psdsql(query)

def get_leagues_and_country() -> pd.DataFrame:
    query = 'Select l.name as league_name, c.name as country_name from League l join Country c on l.country_id  = c.id;'
    return __psdsql(query)

def get_seasons() -> pd.DataFrame:
    query = 'Select distinct(season) from Match m'
    return __psdsql(query)

def get_leagues_stats(season:str = '') -> pd.DataFrame:
    query = """Select l.name as League,c.name as Country, m.season as Season,
        count(distinct m.stage) as Games,
        max(max(m.home_team_goal), max(m.away_team_goal)) as MaxGoals,
        Round(avg(m.home_team_goal),2) as Average_Goals_By_Home,
        Round(avg(m.away_team_goal), 2) as Average_Goals_By_Away,
        Avg(m.away_team_goal + m.home_team_goal) as Average_Difference_Goals,
        Round(avg(m.away_team_goal + m.home_team_goal), 2) as Average_Goals,
        Sum(m.home_team_goal + m.away_team_goal) as Total_Goals
        from League l 
        join Country c on l.country_id  = c.id
        join Team t1  on t1.team_api_id  = m.home_team_api_id  
        join Team t2 on t2.team_api_id  = m.away_team_api_id 
        join "Match" m  on m.country_id  = c.id """
    if len(season) > 0:
        query += f"""WHERE season = '{season}' """ 
    query +="""
        group by c.name, m.season
        order by c.name, m.season
        """
    df = __psdsql(query)
    df.index = df.League
    return df