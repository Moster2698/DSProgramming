import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def plot_games_per_season(df: pd.DataFrame):
    sns.barplot(df, y = df.Season, x= df.Games_Played, hue=df.League, )
    plt.title('Games played Over Years')
    plt.ylabel('Games Played')
    plt.xlabel('Seasons')

def plot_cards_per_season(df: pd.DataFrame):
    sns.barplot(df, x=df.index, y=df.games_with_card)
    plt.title(f'2008-2016 games with at least one red or yellow card')
    plt.xlabel('Seasons')
    plt.ylabel('Number of games with cards')

def plot_featuers(df: pd.DataFrame):
    ax: plt.Axes
    columns = df.columns[4:]
    rows = st.columns(2)
    i = 0
    countries = df.Country.unique()
    for column in columns:
        df_c = pd.DataFrame(index=np.sort(df['Season'].unique()), columns=df['Country'].unique())
        for country in countries:
            df_c.loc[:, country] = list(df.loc[df['Country']==country,column])
        i+=1
        rows[(i)%2].pyplot(df_c.plot(rot=45, title=column).figure)