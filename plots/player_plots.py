import typing
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
def plot_players_attributes(df):
    rows = st.columns(2)
    rows[0].markdown('### Overall Rating of players')
    plot_overall_rating(df, rows[0])
    rows[1].markdown('### Potential of players')
    plot_potential(df, rows[1])

def plot_overall_rating(df: pd.DataFrame, row):
    ax: plt.Axes
    fig, ax = plt.subplots()
    ax.hist(df.overall_rating, bins=20)
    plt.xlabel('Overall Rating')
    plt.ylabel('# Players')
    plt.title('OVERALL RATING')
    row.pyplot(fig)

def plot_potential(df: pd.DataFrame, row):
    ax: plt.Axes
    fig, ax = plt.subplots()
    ax.hist(df.potential, bins=20)
    plt.xlabel('Overall Rating')
    plt.ylabel('# Players')
    plt.title('OVERALL RATING')
    row.pyplot(fig)