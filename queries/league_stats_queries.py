import pandas as pd
import streamlit as st
import sqlite3

def __get_connection() -> sqlite3.Connection:
    """
    Private method which opens a connection when called, remember to close it when used.s
    """
    return sqlite3.connect('database.sqlite')
def __psdsql(query:str) -> pd.DataFrame:
    """
    Private method which executes the query passed by argument and returns it as a dataframe.
    """
    try:
        conn = __get_connection()
        df = pd.read_sql_query(query, __get_connection())
        conn.close()
        return df
    except Exception as e:
        st.write(e)
        return None
    
def get_table_stats_by_season_and_country(season:str, country: str) -> pd.DataFrame:
    """
    Return as a pandas dataframe the table stats of a specific season and country.

    """
    query = f"""SELECT t.team_long_name as Team, 
    3*(h.wins + a.wins) + (h.draws + a.draws) as Points,
    (h.wins + a.wins) as Wins, (h.draws + a.draws) as Draws, (h.losses + a.losses) as Losses, (h.goals + a.goals) as Goal_Done,
    (h.goals_received + a.goals_received) as Goal_Received
    FROM home_stats h 
    JOIN away_stats a
    On h.team = a.team and h.season = a.season
    JOIN team t on h.team = t.team_api_id 
    JOIN Country c on h.country = c.id
    WHERE h.season = '{season}'
    AND c.name = '{country}' 
    Order by h.name, h.season, Points Desc, (h.goals + a.goals) desc"""
    df = __psdsql(query)
    return df

    
def get_leagues() -> pd.DataFrame:
    """
    Returns as a pandas dataframe all the information available for the leagues
    """
    query = 'Select * from League'
    return __psdsql(query)

def get_country() -> pd.DataFrame:
    """
    Return a dataframe which contains all the countries present in the dataframe.
    """
    query = 'Select name from Country'
    return __psdsql(query)

def get_leagues_and_country() -> pd.DataFrame:
    """
    Returns a pandas dataframe which contains the league name and country name.
    """
    query = 'Select l.name as league_name, c.name as country_name from League l join Country c on l.country_id  = c.id;'
    return __psdsql(query)
def get_league_name_from_country(country:str) -> str:
    """
    Get the league name for the speicfic country passed as parameter.
    """
    query = f"Select l.name as Name from League l join Country c where c.name = '{country}'"
    try:
        conn = __get_connection()
        cursor = conn.execute(query)
        return cursor.fetchone()[0]
    except Exception  as e:
        print(e)
def get_seasons() -> pd.DataFrame:
    """
    Return the different seasons available in the dataset.
    """
    query = 'Select distinct(season) from Match m'
    return __psdsql(query)

def get_leagues_stats(season:str = '') -> pd.DataFrame:
    """
    Get the league stats by season, if the season is not specified then the method returns all the league stats.
    """
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

def get_cards_game_per_season_and_country() -> pd.DataFrame:
    """
    Returns as a pandas dataframe the games in which a yellow or red card has been given.
    """
    query =f'''SELECT m.season as Season ,Count(goal) as games_with_card
    FROM Match m
    Join Country c
    on m.country_id = c.id
    WHERE ((card LIKE '%>y<%') OR (card LIKE '%>r<%'))
    GROUP by m.season
    Order by m.season, games_with_card desc'''
    df = __psdsql(query)
    df.index = df['Season']
    df.drop(labels=['Season'],axis=1, inplace=True)
    return df

def get_games_played() -> pd.DataFrame:
    """
    Returns as a pandas dataframe the total number of games played in each league and season.
    """
    query = '''Select l.name as League , m.season as Season,Count(m.stage) as Games_Played from "Match" m
        Join League l
        on m.league_id  = l.id
        Group by m.Season, l.name;'''
    return __psdsql(query)
