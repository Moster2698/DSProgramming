from typing import List
import pandas as pd
import streamlit as st
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import queries.players_stats as queries
sns.set_style('darkgrid')

def plot_players_attributes(df, columns: List[str], rows ):
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
def plot_violin_plot_by_name(df: pd.DataFrame, columns: List[str]):
    if len(columns) > 0:
        ax: plt.Axes
        fig, ax = plt.subplots()
        ax = sns.violinplot(df[columns])
        return fig     

def plot_attribute_hist_by_name(df: pd.DataFrame, columns:List[str], row):
    if len(columns) > 0:
        ax: plt.Axes
        fig, ax = plt.subplots()
        ax = sns.kdeplot(df[columns], fill=True)
        row.pyplot(fig)
def plot_foot_ratings():
    fig = plt.figure(figsize=(15,5))
    plt.subplot(1,2,1)
    plt.title('Ratings of Right Footed Players')
    sns.histplot(data = queries.get_ratings_from_foot('right')['avg_rating'], bins=60)
    plt.xlabel('Average Rating')
    plt.ylabel('Count')
    plt.subplot(1,2,2)
    plt.title('Ratings of Left Footed Players')
    sns.histplot(data = queries.get_ratings_from_foot('left')['avg_rating'], bins=60)
    plt.xlabel('Average Rating')
    plt.ylabel('Count')
    st.pyplot(fig)

def plot_correlation_heatmap(df: pd.DataFrame):
    corr = df[df.columns[1:]].corr()
    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))
    # Set up the matplotlib figure
    fig = plt.figure(figsize=(30, 15))

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, cmap="Blues",annot=True)
    st.pyplot(fig)

def plot_correlation_heatmap_overall(df: pd.DataFrame):
    corr = df.corr()
    # Generate a mask for the upper triangle
    x = corr[['overall_rating']]
    x = x.sort_values(by='overall_rating', ascending=False)
    mask = np.triu(np.ones_like(x, dtype=bool))
    # Set up the matplotlib figure
    fig = plt.figure(figsize=(30, 20))
    
    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(x, cmap="Blues",annot=True)
    st.pyplot(fig)
