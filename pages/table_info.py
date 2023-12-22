import streamlit as st
import pandas as pd
import functions
from typing import List
import typing
import io
import player_plots

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


tables_info, table_names = functions.get_tables_infos()
if len(table_names) == 0:
    st.write('Error fetching Data')
else:
    option = st.selectbox('Select Table', table_names,key='table', on_change=on_selectbox_change)
    if table_names.index(option) >= 0:
        table_to_show = tables_info[table_names.index(option)]
        write_html('<h1> Table Data </h1>')
        st.dataframe(table_to_show[:100], hide_index=True)
        rows = st.columns(2)
        rows[0].markdown("### Table description")
        rows[0].dataframe(table_to_show.describe().T)
        buf = io.StringIO()
        table_to_show.info(buf=buf)
        rows[1].markdown('### Table info')
        columns_chosen = [x for x in dataframe_with_selections(get_df_info(buf), rows[1]).Column]
        player_plots.plot_players_attributes(table_to_show, columns_chosen)
    else:
        print(option)