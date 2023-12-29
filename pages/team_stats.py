import streamlit as st
from queries import team_queries
from plots import team_plots
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
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
st.markdown("### None Values")
st.markdown(f'''I've decided to replace the None values with the mean because even though
            over {round((1458-489)/1458 * 100,2) } % of the data is None values I need the column for calculating a metrics that
            will be useful nextly.''')
st.markdown(f'''In the new dataset that I'm going to use for the plotting I introduced the team_names, the season 
            where the statistics are taken and then the overall, which is the sum of all numeric features and that will be
            our metrics. The dataset will be the folliwng:''')
team_attributes = team_queries.get_most_overall()
st.dataframe(team_attributes)
st.markdown('## Data visualization and EDA')
st.markdown('''This section will focus on the plot of interesting features and some EDA.''')
st.markdown('### Top winrate teams')
st.markdown('''I start with the most winning clubs overall.Defined the winrate as $$wr = \dfrac{wins}{games} $$. The dataframe that I got is the following:''')
team_winrates = team_queries.get_win_rate()
st.dataframe(team_winrates)
team_plots.plot_winrate(team_winrates[:10])
st.markdown('The most winning team is FC Barcelona, with 73% of winrate')
('### Top goals done by teams')
team_goals = team_queries.get_most_goals_done_all_time()
st.dataframe(team_goals)
"""team_attributes['buildUpPlayDribbling'].replace('None', np.nan, inplace=True)
team_attributes['buildUpPlayDribbling'].fillna(team_attributes['buildUpPlayDribbling'].mean(), inplace=True)
st.markdown('Replace the null values with the mean')
team_attributes['buildUpPlayDribbling'] = team_attributes['buildUpPlayDribbling'].astype(np.int64) 
buf = io.StringIO()
team_attributes.info(buf=buf)
st.dataframe(team_queries.f.get_df_info(buf))
number_columns = team_attributes.select_dtypes(include=[np.number])
number_columns = number_columns.columns[3:]
team_attributes['overall'] = team_attributes[number_columns].sum(axis=1)
interestings_df = team_attributes[['team_api_id','overall', 'date']]
interestings_df.sort_values(by='overall', ascending=False, inplace=True)
interestings_df['date'] = pd.to_datetime(interestings_df['date'])
interestings_df.index = interestings_df['date']
fig = plt.figure(figsize=(10,6))
plt.plot(interestings_df, )
st.pyplot(fig)
"""


