import queries.league_stats_queries as queries
import plots.leagues_plots as plots
import streamlit as st
import seaborn as sns
import pandas as pd
from typing import List
import matplotlib.pyplot as plt
import numpy as np
import functions


        
st.markdown('# League statistics\n')
st.markdown("In this page we're looking for the statistics of the matches played and the ordinary statistics such as average goals per games, max goals per seasons and so on.")

st.markdown('## Leagues and Countries')
st.dataframe(queries.get_leagues_and_country(), hide_index=True)

league_stats_df = queries.get_leagues_stats()

st.markdown('## Leagues and statistics')
st.dataframe(league_stats_df, hide_index=True)
plots.plot_featuers(league_stats_df)
fig = plt.figure(figsize=(8,14))
plots.plot_games_per_season(queries.get_games_played())
st.pyplot(fig)
st.markdown('### What happened in the 2013/2014 in Belgium?')
st.markdown('If we see in the dataframe in that season, then the result is the following:')
df = league_stats_df[(league_stats_df.Country == 'Belgium') & (league_stats_df.Season == '2013/2014')]
st.dataframe(df)
card_games_df = queries.get_cards_game_per_season_and_country()
if(card_games_df.size > 0):
    st.markdown('## Games with yellow or red cards')
    fig = plt.figure(figsize=(10,6))
    plots.plot_cards_per_season(card_games_df)
    st.pyplot(fig)
            
detailed_matches = functions.get_detailed_matches_by_season()

st.markdown('## Matches details')
rows = st.columns(3)
season = rows[0].selectbox('Select Season', options = queries.get_seasons(), index=0)
country = rows[1].selectbox('Select Country', options = queries.get_country(), index=0)
mask = True
if len(season) > 0:
    mask &= detailed_matches.Season == season
if len(country) > 0:
    mask &= detailed_matches.Country == country
st.markdown('League Matches')
st.dataframe(detailed_matches[detailed_matches.columns[4:]][mask], hide_index=True)
if len(season) > 0 and len(country) > 0:
    df = queries.get_table_stats_by_season_and_country(season, country)
    if df is not None:
        st.markdown('League Summary')
        st.dataframe(queries.get_table_stats_by_season_and_country(season, country), hide_index=True)
        


