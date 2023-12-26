import pandas as pd
import streamlit as st
import numpy as np
import queries.players_stats as queries
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt

df = queries.get_players_attributes()
if df is not None:
    st.dataframe(df.head())
    st.write(df.shape)
    st.write(df.columns)
    features = ['potential', 'crossing', 'finishing', 'heading_accuracy',
       'short_passing', 'volleys', 'dribbling', 'curve', 'free_kick_accuracy',
       'long_passing', 'ball_control', 'acceleration', 'sprint_speed',
       'agility', 'reactions', 'balance', 'shot_power', 'jumping', 'stamina',
       'strength', 'long_shots', 'aggression', 'interceptions', 'positioning',
       'vision', 'penalties', 'marking', 'standing_tackle', 'sliding_tackle',
       'gk_diving', 'gk_handling', 'gk_kicking', 'gk_positioning',
       'gk_reflexes']
    target = ['overall_rating']
    df = df.dropna()
    X = df[features]
    st.write(features)
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.33,random_state=42)
    regressor = LinearRegression()
    regressor.fit(X_train,y_train)
    y_prediction = regressor.predict(X_test)
    st.write(y_prediction)
    st.write(".............Evaluation metrics for Linear Regression..............")
    score = regressor.score(X_test, y_test)
    n=len(df[target])
    p=len(features)
    adjr= 1-(1-score)*(n-1)/(n-p-1)
    st.write("RSquared: ",score)
    st.write("AdjustedRSquared: ",adjr)
    st.write('MAE', metrics.mean_absolute_error(y_test, y_prediction))
    st.write('MSE', metrics.mean_squared_error(y_test, y_prediction))
    st.write('RMSE', np.sqrt(metrics.mean_squared_error(y_test, y_prediction)))
    regressor = DecisionTreeRegressor(max_depth=20)
    regressor.fit(X_train,y_train)
    y_prediction = regressor.predict(X_test)
    st.write(".............Evaluation metrics for Linear Regression..............")
    score = regressor.score(X_test, y_test)
    n=len(df[target])
    p=len(features)
    adjr= 1-(1-score)*(n-1)/(n-p-1)
    st.write("RSquared: ",score)
    st.write("AdjustedRSquared: ",adjr)
    st.write('MAE', metrics.mean_absolute_error(y_test, y_prediction))
    st.write('MSE', metrics.mean_squared_error(y_test, y_prediction))
    st.write('RMSE', np.sqrt(metrics.mean_squared_error(y_test, y_prediction)))
