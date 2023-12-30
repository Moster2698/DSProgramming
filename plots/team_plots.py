from typing import List
import pandas as pd
import streamlit as st
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

def plot_winrate(df:pd.DataFrame):
    f, ax = plt.subplots(figsize=(10, 6))
    # Plot the total crashes
    sns.set_color_codes("pastel")
    sns.barplot(x="P", y="team_long_name", data=df,
                label="Games Played", color="b")

    # Plot the crashes where alcohol was involved
    sns.set_color_codes("muted")
    sns.barplot(x="V", y="team_long_name", data=df,
                label="Games won", color="b")

    # Add a legend and informative axis label
    ax.legend(ncol=2, loc="lower right", frameon=True)
    plt.title('Top 10 most winrates teams')
    ax.set(xlim=(0, 500), ylabel="",
        xlabel="Games")
    sns.despine(left=True, bottom=True)
    st.pyplot(f)

def plot_goals_done(df: pd.DataFrame):
    fig = plt.figure(figsize=(10,6))
    sns.set_color_codes("pastel")
    sns.barplot(x="team_long_name", y="Gd", data=df, color="b")
    plt.title(' Top 10 most scoring teams')
    plt.xticks(rotation=45)
    plt.ylabel('Goals')
    plt.xlabel('Teams')
    st.pyplot(fig)

def plot_points_done(df: pd.DataFrame):
    fig = plt.figure(figsize=(10,6))
    sns.set_color_codes("pastel")   
    sns.barplot(x="team_long_name", y="Points", data=df, color="b")
    plt.title(' Top 10 teams with most points done')
    plt.xticks(rotation=45)
    plt.ylabel('Goals')
    plt.xlabel('Teams')
    st.pyplot(fig)

def plot_overall(df: pd.DataFrame):
    fig = plt.figure(figsize=(10,6))
    sns.set_color_codes("pastel")
    sns.barplot(x="team_long_name", y="overall", data=df, color="b")
    plt.title(' Top 10 teams with most overall')
    plt.xticks(rotation=45)
    plt.ylabel('Overall')
    plt.xlabel('Teams')
    st.pyplot(fig)

def plot_correlation_points_overall(df: pd.DataFrame):
    corr = df[df.columns[1:]].corr()
    # Generate a mask for the upper triangle
    fig = plt.figure(figsize=(10, 6))
    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, cmap=plt.cm.Reds,annot=True)
    st.pyplot(fig)