import queries.league_stats_queries as queries
import streamlit as st
import seaborn as sns
import pandas as pd
from typing import List
import matplotlib.pyplot as plt
import numpy as np
import functions
def plot_featuers(df: pd.DataFrame):
    ax: plt.Axes
    columns = df.columns[4:]
    rows = st.columns(2)
    i = 0
    countries = df.Country.unique()
    for column in columns:
        df_c = pd.DataFrame(index=np.sort(df['Season'].unique()), columns=df['Country'].unique())
        for country in countries:
            df_c.loc[:, country] = list(df.loc[df['Country']==country,column])
        i+=1
        rows[(i)%2].pyplot(df_c.plot(rot=45, title=column).figure)
        
st.markdown('# League statistics\n')
st.markdown("In this page we're looking for the statistics of the matches played and the ordinary statistics such as average goals per games, max goals per seasons and so on.")

st.markdown('## Leagues and Countries')
st.dataframe(queries.get_leagues_and_country(), hide_index=True)

league_stats_df = queries.get_leagues_stats()

st.markdown('## Leagues and statistics')
st.dataframe(league_stats_df, hide_index=True)

st.markdown('## Plotting of the features')
plot_featuers(league_stats_df)


st.markdown('### What happened in the 2013/2014 in Belgium?')
st.markdown('If we see in the dataframe in that season, then the result is the following:')
df = league_stats_df[(league_stats_df.Country == 'Belgium') & (league_stats_df.Season == '2013/2014')]
st.dataframe(df)

detailed_matches = functions.get_detailed_matches_by_season()

st.markdown('## Matches details')
rows = st.columns(3)
season = rows[1].selectbox('Select Season', options = queries.get_seasons(), index=0)
country = rows[2].selectbox('Select Season', options = queries.get_country(), index=0)
mask = True
if len(season) > 0:
    mask &= detailed_matches.Season == season
if len(country) > 0:
    mask &= detailed_matches.Country == country
st.dataframe(detailed_matches[mask])
if len(season) > 0 and len(country) > 0:
    st.dataframe(queries.get_table_stats_by_season_and_country(season, country))

