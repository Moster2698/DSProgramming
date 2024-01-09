import streamlit as st
import pandas as pd
import functions
from typing import List
import time
import io
import os
import plots.player_plots as plots


table_to_show = None
st.set_page_config(layout="wide")

def is_database_installed():
    path = 'database.sqlite'
    return os.path.isfile(path)

def dataframe_with_selections(df):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn()},
        disabled=df.columns,
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop('Select', axis=1)

def create_main_page():
    st.markdown('# What is the dataset')
    st.markdown('''European Soccer (Football) Database is an open-source database based in the SQLite database engine available 
                on Kaggle for use in data analysis and machine learning projects. 
                The database contains information about more than 25,000 matches and 10,000 players,
                and nearly 300 teams across football leagues in 11 countries in Europe between the 2008/2009 and 2015/2016
                season sourced from multiple websites. Additionally, the database also contains information about weekly 
                updated player attributes and ratings sourced from corresponding yearly instalments of the FIFA franchise f
                rom Electronic Arts and EA SPORTS, and betting odds from up to 10 odds providers.''')
    st.markdown('## Data exploratory')
    st.markdown('''On this page, you can choose the table for which you wish to retrieve fundamental details, including the quantity of values, column types, basic statistics, and simple visualizations. ''')
    st.markdown('### Database architecture')
    st.markdown('The dataset is contained in a database file, more precisely is a sqlite type of a RDBMS database which is not that different from the usual SQL. The unique difference that matters for us is that SQlite is more lightweight and allows only one users. The architecture of the database is shown in the next image')
    rows = st.columns([0.25, 0.5, 0.25])
    rows[1].image('./assets/db_architecture.png', caption='Architecture of the database', width=500)
    st.markdown('The tables represent which kind of data we have to deal with, there are in total 7 tables and each of them has a primary key (the one in bold) which identifies each row of the tables. The links show that there is a relationship between the tables involved and usually those links are between foreign_keys.')
    tables_info, table_names = functions.get_tables_infos()
    if len(table_names) == 0:
        st.write('Error fetching Data')
    else:
        form = st.form('input_box',clear_on_submit=False, border=False)
        rows = form.columns([0.6, 0.4])
        option = rows[0].selectbox('Select Table', table_names, key='table')
        rows[1].write('')
        rows[1].write('')
        btn_submitted = rows[1].form_submit_button('Submit')
        if btn_submitted:
            if table_names.index(option) >= 0:
                table_to_show = tables_info[table_names.index(option)]
                st.markdown(f'Dataframe Size: {round(table_to_show.memory_usage(deep=True).sum() / 1024 / 1024,2)} MB')
                st.markdown('''## Table data''')
                st.dataframe(table_to_show, hide_index=True)  
                st.markdown("### Table description")
                st.dataframe(table_to_show.describe().T)
                st.markdown('### Table info')
                buf = io.StringIO()
                if option == 'Match':
                    table_to_show[table_to_show.columns[:-30]].info(buf=buf)
                else:
                    table_to_show.info(buf=buf)
                df = functions.get_df_info(buf)
                st.dataframe(df)
                if option == 'Match':
                    st.markdown(''' The table Match contains informations about the all the matches done in the seasons 2008-2016. It also contains 
                                information about the stats of the game such as possession, goals done, goals done by home team and then it also have
                                bettings from ten different providers for each game. Each betting site has three different types of betting depending on the result of the game: win, draw, loss.
                                For the whole project i decided to not use those columns because those were not useful for what i wanted to show, moreover i decided to drop the
                                formations lineup noted by the columns containing the big X on the right of the name.''')
                
            else:
                print(option)
def hide_warning():
    st.markdown("""
    <style>
        #warning{
            display: none;
        }
        #warning-body{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)
def hide_side_bar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)
def show_side_bar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: block;
        }
    </style>
    """, unsafe_allow_html=True)
def create_warning():
    hide_side_bar()
    st.markdown('<h1 id="warning-title"> Warning</h1>',unsafe_allow_html=True)
    st.markdown('''<p id="warning-body">The application cannot start as it is unable to locate the essential database in your current working directory. To resolve this issue, kindly download the required database by following the link provided: <a href="https://www.kaggle.com/datasets/hugomathien/soccer/download?datasetVersionNumber=10">download</a></p>''',unsafe_allow_html=True)
    with st.spinner('Waiting for the database to be installed in the working directory'):
        while True:
            if is_database_installed():
                functions.create_views()
                hide_warning()
                show_side_bar()
                create_main_page()
                break
            time.sleep(2.5)
if is_database_installed():
    hide_warning()
    create_main_page()
else:
    create_warning()
