from typing import List
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import scipy
sns.set_style('darkgrid')
def plot_players_attributes(df, columns: List[str] ):
    rows = st.columns(2)
    rows[0].markdown('### Density Functions')
    plot_attribute_hist_by_name(df, columns, rows[0])
    rows[1].markdown('### Distribution Function')
    plot_cumulative_dist(df, columns, rows[1])

def plot_cumulative_dist(df: pd.DataFrame, columns: List[str], row):
    if len(columns) > 0:
        ax: plt.Axes
        fig, ax = plt.subplots()
        ax = sns.kdeplot(df[columns], cumulative=True)
        row.pyplot(fig)
def plot_violin_plot_by_name(df: pd.DataFrame, columns: List[str], row):
    if len(columns) > 0:
        ax: plt.Axes
        fig, ax = plt.subplots()
        ax = sns.violinplot(df[columns])
        row.pyplot(fig)     

def plot_attribute_hist_by_name(df: pd.DataFrame, columns:List[str], row):
    if len(columns) > 0:
        ax: plt.Axes
        fig, ax = plt.subplots()
        ax = sns.kdeplot(df[columns], shade=True)
        row.pyplot(fig)
