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