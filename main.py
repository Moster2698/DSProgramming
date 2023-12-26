import streamlit as st
import pandas as pd
import functions
from typing import List
import typing
import io
import plots.player_plots as plots



table_to_show = None
st.set_page_config(layout="wide")
def on_selectbox_change():
    option = st.session_state['table']
    

def write_html(html:str):
      st.write(html, unsafe_allow_html=True)
def dataframe_with_selections(df, row):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = row.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn()},
        disabled=df.columns,
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop('Select', axis=1)
def get_df_info(buffer):
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
option = ''

st.markdown('# What is the dataset')
st.markdown('''European Soccer (Football) Database is an open-source database based in the SQLite database engine available 
            on Kaggle for use in data analysis and machine learning projects. 
            The database contains information about more than 25,000 matches and 10,000 players,
             and nearly 300 teams across football leagues in 11 countries in Europe between the 2008/2009 and 2015/2016
             season sourced from multiple websites. Additionally, the database also contains information about weekly 
            updated player attributes and ratings sourced from corresponding yearly instalments of the FIFA franchise f
            rom Electronic Arts and EA SPORTS, and betting odds from up to 10 odds providers.''')
st.markdown('## Data exploratory')
st.markdown('''In this page you'll be able to select the table of which you want to gather some basic information
            such as the number of values, type of the columns involved, ordinary statistics and some basic plots. ''')
tables_info, table_names = functions.get_tables_infos()
if len(table_names) == 0:
    st.write('Error fetching Data')
else:
    option = st.selectbox('Select Table', table_names, key='table', on_change=on_selectbox_change)
    if table_names.index(option) >= 0:
        table_to_show = tables_info[table_names.index(option)]
        st.markdown(f'Dataframe Size: {table_to_show.memory_usage(deep=True).sum() / 1024 / 1024} MB')
        st.markdown('''## Table data''')
        st.dataframe(table_to_show[:100], hide_index=True)  
        rows = st.columns(2)
        rows[0].markdown("### Table description")
        rows[0].dataframe(table_to_show.describe().T)
        buf = io.StringIO()
        table_to_show.info(buf=buf)
        rows[1].markdown('### Table info')
        selection = dataframe_with_selections(get_df_info(buf), rows[1])
        columns_selected = selection[(selection.Dtype == 'int64') | (selection.Dtype == 'float64')]
        rows = st.columns(2)
        if len(columns_selected) > 0:
            plots.plot_players_attributes(table_to_show, columns_selected, rows)
    else:
        print(option)