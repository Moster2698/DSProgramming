import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import functions 
import streamlit as st
st.title('Test')


detailed_matches = functions.get_detailed_matches_by_season('2010/2011')
if detailed_matches is not None:
    #Search the max number of goals in a game
    max_goals_home =  detailed_matches.home_team_goal.max()
    max_goals_away =  detailed_matches.away_team_goal.max()

leagues_details = functions.get_season_information()
fig,ax = plt.subplots()

ax.plot(leagues_details.index, leagues_details)
st.pyplot(fig=fig)

