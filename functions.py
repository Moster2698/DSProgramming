import sqlite3
import pandas as pd
import numpy as np
import streamlit as st
from typing import List
st.cache_data
def get_connection():
    return sqlite3.connect('database.sqlite')
@st.cache_data
#Ritorna i nomi e i dati relativi alle tabelle presenti nel dataset
def get_tables_infos()->(List[pd.DataFrame], List[str]):
    query = """SELECT name FROM sqlite_master WHERE type='table' and name <> 'sqlite_sequence';"""
    dfs = list()
    names = list()
    query_result = psdsql(query)
    if query_result is not None:
        for table in query_result.name:
            query = f"""SELECT * FROM {table}"""
            df = psdsql(query)
            if df is not None:
                dfs.append(df)
                names.append(table)
                df.index = df[df.columns[0]]
    return dfs, names
@st.cache_data
def get_detailed_matches_by_season()->pd.DataFrame:
    query = f"""SELECT Match.id, 
            Country.name AS Country, 
            League.name AS League, 
            season as Season, 
            stage as Game, 
            HT.team_long_name AS  home_team,
            AT.team_long_name AS away_team,
            home_team_goal, 
            away_team_goal                                        
    FROM Match
    JOIN Country on Country.id = Match.country_id
    JOIN League on League.id = Match.league_id
    LEFT JOIN Team AS HT on HT.team_api_id = Match.home_team_api_id
    LEFT JOIN Team AS AT on AT.team_api_id = Match.away_team_api_id
    ORDER by date;"""
    return psdsql(query)

def get_df_info(buffer) -> pd.DataFrame:
     lines = buffer.getvalue ().split ('\n')
     # lines to print directly
     lines_to_print = [0, 1, 2, -2, -3]
     # lines to arrange in a df
     list_of_list = []
     for x in lines [5:-3]:
         list = x.split ()
         list_of_list.append (list)
     info_df = pd.DataFrame (list_of_list, columns=['index', 'Column', 'Non-null-Count', 'null', 'Dtype'])
     info_df.drop (columns=['index', 'null'], axis=1, inplace=True)
     return info_df

def psdsql(query:str) -> pd.DataFrame:
    try:
        return pd.read_sql(query, get_connection())
    except:
        return None