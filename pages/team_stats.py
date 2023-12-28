import streamlit as st
from queries import team_queries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
team_attributes = team_queries.get_teams_attributes()
st.dataframe(team_attributes, hide_index=True)
buf = io.StringIO()
team_attributes.info(buf=buf)
st.dataframe(team_queries.f.get_df_info(buf))
st.dataframe(team_attributes.describe().T)
team_attributes['buildUpPlayDribbling'].replace('None', np.nan, inplace=True)
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