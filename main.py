import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import functions 
import streamlit as st
import sys
from os.path import dirname
st.title('Test')
sys.path.append(dirname('plots/player_plots.py'))

leagues_details = functions.get_season_information()
fig,ax = plt.subplots()

ax.plot(leagues_details.index, leagues_details)
st.pyplot(fig=fig)

