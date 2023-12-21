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
option = st.selectbox('Select Table', table_names,key='table', on_change=on_selectbox_change)
if table_names.index(option) >= 0:
    table_to_show = tables_info[table_names.index(option)]
    write_html('<h1> Table Data </h1>')
    st.dataframe(table_to_show, hide_index=True)
    rows = st.columns(2)
    rows[0].markdown("### Table description")
    rows[0].dataframe(table_to_show.describe().T)
    buf = io.StringIO()
    table_to_show.info(buf=buf)
    rows[1].markdown('### Table info')
    rows[1].dataframe(get_df_info(buf))
    if option == 'Player_Attributes':
        player_plots.plot_players_attributes(table_to_show)
else:
      print(option)