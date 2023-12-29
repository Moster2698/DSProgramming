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
    plt.title('Top ten most winrates teams')
    ax.set(xlim=(0, 500), ylabel="",
        xlabel="Games")
    sns.despine(left=True, bottom=True)
    st.pyplot(f)

    