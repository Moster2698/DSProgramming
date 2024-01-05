import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def plot_games_per_season(df: pd.DataFrame):
    sns.barplot(df, y = df.Games_Played, x= df.Season, hue=df.League, )
    plt.title('Games played Over Seasons 2008-2016')
    plt.ylabel('Games Played')
    plt.xlabel('Seasons')

def plot_cards_per_season(df: pd.DataFrame):
    sns.barplot(df, x=df.index, y=df.games_with_card)
    plt.title(f'2008-2016 games with at least one red or yellow card')
    plt.xlabel('Seasons')
    plt.ylabel('Number of games with cards')

def plot_bar_stacked_per_season(df:pd.DataFrame, column:str):
    sns.barplot(df, x=df.index, y =df[column])
    plt.xlabel('Seasons')

def plot_featuers(df: pd.DataFrame):
    columns = df.columns[4:]
    rows = st.columns(2)
    i = 0
    for column in columns:
        fig = plt.figure(figsize=(10,6))
        sns.lineplot(data = df,x='Season', y=column, hue='Country', style='Country',markers='*' )
        plt.xlabel('Seasons')
        plt.ylabel(column)
        rows[(i)%2].pyplot(fig)
        i +=1
       