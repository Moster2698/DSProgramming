import streamlit as st
import pandas as pd
import functions
tables_info = functions.get_tables_infos()

for table in tables_info:
    st.dataframe(table)