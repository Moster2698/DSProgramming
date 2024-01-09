import streamlit as st
from queries import team_queries
from plots import team_plots
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
st.set_page_config(layout="wide")
st.markdown('# Team statistics')
st.markdown("""This section start with a little description of what part of the dataset I used which is the 
            <i>team_attributes</i>. In the second part I do data cleaning of the table because for mine purposes it has some null values
            which are there because the data is taken from scraping and the author too said that some of the data is not accurate.
            The last part focus on the data visualization and extrapolating useful information about the teams. """, unsafe_allow_html=True)
st.markdown('## First Part: Data Description')
team_attributes = team_queries.get_teams_attributes()
st.markdown('''The table team_attributes contains different characteristics of the teams present in the fifa dataset between the seasons 2008-2016.
            The content of the table is the following:''')
st.dataframe(team_attributes, hide_index=True)
buf = io.StringIO()
team_attributes.info(buf=buf)
st.markdown('''Then the informations of the table are displayed''')
st.dataframe(team_queries.f.get_df_info(buf))
st.markdown(f'''We note that the total number of None values in the <i>buildUpPlayDribbling</i> are 489 and in the other columns
            there are not None values. Lastly displayed is the description of the table''', unsafe_allow_html=True)
st.dataframe(team_attributes.describe().T)
st.markdown('## Second Part: Data Cleaning')
st.markdown("""This section focuses on the cleaning of the table and the procedure is focused in two parts: 
            <ul> 
            <li> Decide what to do with the None values;
            <li> Removing the columns in which we are not interested in for the plottings
            </ul>""",unsafe_allow_html=True)
st.markdown("### None Values and removing columns")
st.markdown(f'''I've decided to replace the None values with the mean because even though
            over {round((1458-489)/1458 * 100,2) } % of the data is None values I need the column for calculating a metrics that
            will be useful nextly.''')
st.markdown(f'''In the new dataset that I'm going to use for the plotting I introduced the team_names and the overall, which is the sum of all numeric features and that will be
            our metrics. The dataset will be the folliwng:''')
team_attributes = team_queries.get_most_overall()
st.dataframe(team_attributes)
st.markdown('All the other columns were removed because they were not relevant for the next computations.')
st.markdown('## Data visualization and EDA')
st.markdown('''This section will focus on the plot of interesting features and some EDA.''')
team_plots.plot_overall(team_queries.get_most_overall())
st.markdown('### Top winrate teams')
st.markdown('''I start with the most winning clubs overall.Defined the winrate as $$wr = \dfrac{wins}{games} $$. The dataframe that I got is the following:''')
team_winrates = team_queries.get_win_rate()
team_plots.plot_winrate(team_winrates[:10])
st.markdown('The most winning team is FC Barcelona, with 73% of winrate')
st.markdown('### Top goals done by teams')
st.markdown('''Another interesting metrics to determine if the team is a good one is the amount of total goals done.''')
team_goals = team_queries.get_most_goals_done_all_time()
team_plots.plot_goals_done(team_goals[:10])
st.markdown('### Teams with most points')
team_points = team_queries.get_most_points()
team_plots.plot_points_done(team_points[:10])
st.markdown('### Points and overall')
st.markdown('In this last section we will see if there is some correlation between the total number of points done and the maximum overall of the squad:')
team_overall_points = team_queries.get_points_and_max_overall()
st.dataframe(team_overall_points)
fig = plt.figure(figsize=(6, 6))
plt.title('Scatter plot with regression line')
team_plots.plot_correlation_points_overall(team_overall_points)
st.pyplot(fig)
st.markdown('''From what we're seeing there is not a linear relationship between the overall of the stats of a squad and the total number of points that it has done and to prove that we need to calculate the correlation coefficient''')
corr = round(team_overall_points['overall'].corr(team_overall_points['Gd']),2)
st.markdown(f'Correlation between overall and points done is {corr}' )
