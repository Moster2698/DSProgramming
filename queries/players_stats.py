import streamlit as st
import sqlite3
import pandas as pd
import functions as f
def get_players():
    query = 'Select * from Player'
    return f.psdsql(query)
def get_players_attributes():
    query = 'Select * from Player_Attributes'
    return f.psdsql(query)
def get_non_unique_stats():
    query = """Select p.player_name as Player, p.height, p.weight, pa.* from Player p JOIN Player_Attributes pa on p.player_api_id = pa.player_api_id Order by p.player_name asc"""
    return f.psdsql(query)
def get_player_stats():
    query = """Select p.player_name as Player,
    p.height as Height,
    p.weight as Weight,
	AVG(overall_rating) AS "Overall_Rating", 
    AVG(potential) AS "Potential", 
    AVG(crossing) AS "Crossing", 
    AVG(finishing) AS "Finishing",
    AVG(heading_accuracy) AS "Head_Accuracy",
    AVG(short_passing) AS "Short_Passing",
    AVG(volleys) AS "Volleys",
    AVG(dribbling) AS "Dribbling",
    AVG(curve) AS "Curve",
    AVG(free_kick_accuracy) AS "Free_Kick_Accuracy",
    AVG(long_passing) AS "Long_Passing",
    AVG(ball_control) AS "Ball_Control",
    AVG(acceleration) AS "Acceleration",
    AVG(sprint_speed) AS "Sprint_Speed",
    AVG(agility) AS "Agility",
    AVG(reactions) AS "Reactions",
    AVG(balance) AS "Balance",
    AVG(shot_power) AS "Short_Power",
    AVG(jumping) AS "Jumping",
    AVG(stamina) AS "Stamina",
    AVG(strength) AS "Strength",
    AVG(long_shots) AS "Long_Shots",
    AVG(aggression) AS "Aggression",
    AVG(interceptions) AS "Interceptions",
    AVG(positioning) AS "Positioning",
    AVG(vision) AS "Vision",
    AVG(penalties) AS "Penalties",
    AVG(marking) AS "Marking",
    AVG(standing_tackle) AS "Standing_Tackle",
    AVG(sliding_tackle) AS "Sliding_Tackle",
    AVG(gk_diving) AS "Goalkeeper_Diving",
    AVG(gk_handling) AS "Goalkeeper_Handling",
    AVG(gk_kicking) AS "Goalkeeper_Kicking",
    AVG(gk_positioning) AS "Goalkeeper_Positioning",
    AVG(gk_reflexes) AS "Goalkeeper_Reflexes"
   	FROM Player_Attributes pa Join Player p  on p.player_api_id  = pa.player_api_id  
  	GROUP BY p.player_api_id Order by p.player_name asc;"""
    return f.psdsql(query)

def get_preferred_foot():
    query = "Select Sum(CASE  WHEN preferred_foot ='left' THEN 1 END) as left, Sum(CASE  WHEN preferred_foot ='right' THEN 1 END) as right  from Player_Attributes pa ;"
    df = f.psdsql(query)
    return [df.left[0], df.right[0]]
    
def get_ratings_from_foot(foot:str):
    if foot != 'left' and foot != 'right':
        return None
    query = f'''SELECT avg_rating FROM 
    (SELECT pl.player_name as name, pa.preferred_foot as pf_foot, SUM(overall_rating)/COUNT(*) as avg_rating
    FROM PLAYER as pl
    JOIN PLAYER_ATTRIBUTES AS pa
    ON pa.player_api_id = pl.player_api_id
    GROUP BY pl.player_name) WHERE pf_foot = '{foot}' '''
    return f.psdsql(query)