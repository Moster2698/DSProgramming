import queries.league_stats_queries as queries
import plots.leagues_plots as plots
import streamlit as st
import seaborn as sns
import pandas as pd
from typing import List
import matplotlib.pyplot as plt
import numpy as np
import functions

st.set_page_config(layout="wide")
st.markdown('# League statistics\n')
st.markdown("In this page we're looking for the statistics of the matches played and the ordinary statistics such as average goals per games, max goals per seasons and so on.")

st.markdown('## Leagues and Countries')
st.markdown('The leagues and the correlated country')
st.dataframe(queries.get_leagues_and_country(), hide_index=True)

league_stats_df = queries.get_leagues_stats()

st.markdown('## Leagues and statistics')
st.markdown('''One way to describe the leagues it's by its statistics which comprehends ''')
st.markdown('''<ul>
                <li>The total number of games played in a Season</li>
                <li>The maximum goals done in a game by a team in a Season</li>
                <li>Average goals in a game from the home team and away team</li>
                <li>Average difference of goals in a season</li>
                <li>Total goals in a Season</li>
            </ul>''',unsafe_allow_html=True)
st.dataframe(league_stats_df, hide_index=True)
st.markdown('''### Plots of the features''')
plots.plot_featuers(league_stats_df)
st.markdown('''### Number of games played''')
st.markdown('''An essential aspect worth examining is the total number of games played in a season by the league. This metric serves as a robust indicator, enabling us to detect any discrepancies in the gathered data. The analysis of games played contributes rigor to our assessment, ensuring a comprehensive evaluation of the season's dynamics and data reliability.''')
fig = plt.figure(figsize=(10,6))
ax = plt.subplot(111)
plots.plot_games_per_season(queries.get_games_played())
ax.legend(bbox_to_anchor=(1., 1.02))
st.pyplot(fig)
st.markdown('We see that the big countries are stabilized at roughly 350 games a year and that sounds plausible because there were around 19/20 teams. Every team is required to participate in both a primary and a return round, facing off against every other team in each of these rounds. Consequently, the total number of games played is twice the count of teams in the league, minus one.')
st.markdown('''However, in the minor leagues, a lower number of games is evident, primarily attributed to the reduced quantity of participating teams. A notable anomaly emerges in the Belgian league during the 2013/2014 season, where the total number of games played is unusually low, standing at 6. Let's investigate more about that''')
st.markdown('### What happened in the 2013/2014 in Belgium?')
st.markdown('If we see in the dataframe in that season, then the result is the following:')
detailed_matches = functions.get_detailed_country_matches()
condition = (detailed_matches.Country == 'Belgium') & (detailed_matches.Season=='2013/2014')
belgium_games_2013_2014 = detailed_matches[condition]
st.dataframe(belgium_games_2013_2014[['Game','home_team','away_team','home_team_goal','away_team_goal']],hide_index=True)
st.markdown('If we see in https://en.wikipedia.org/wiki/2013–14_Belgian_Pro_League for the games played in Belgium on the season 2013/2014 we have that the total number of games played is 30 and not 6!')
card_games_df = queries.get_cards_game_per_season_and_country()
if(card_games_df.size > 0):
    st.markdown('## Games with yellow or red cards')
    fig = plt.figure(figsize=(10,4))
    plots.plot_cards_per_season(card_games_df)
    st.pyplot(fig)
            
st.markdown('## Matches details and Ranking Table')
st.markdown('In this last section we are going to visualize by tables all the games played in a spefic country and on a selected season. Lastly for that season and country the ranking table will be displayed.')
form = st.form('Input_box', clear_on_submit=False, border=False)
rows = form.columns(3)
season = rows[0].selectbox('Select Season', options = queries.get_seasons(), index=0)
country = rows[1].selectbox('Select Country', options = queries.get_country(), index=0)
rows[2].write('')
rows[2].write('')
submitted = rows[2].form_submit_button('Submit')
if submitted:
    mask = True
    mask &= detailed_matches.Season == season
    mask &= detailed_matches.Country == country
    st.markdown('League Matches')
    st.dataframe(detailed_matches[detailed_matches.columns[4:]][mask], hide_index=True)
    if len(season) > 0 and len(country) > 0:
        df = queries.get_table_stats_by_season_and_country(season, country)
        if df is not None:
            st.markdown('League Summary')
            st.dataframe(queries.get_table_stats_by_season_and_country(season, country), hide_index=True)
        


