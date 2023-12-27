import pandas as pd
import streamlit as st
import numpy as np
import queries.players_stats as queries
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns

df = queries.get_players_attributes()
if df is not None:
   st.dataframe(df.head())
   rows = st.columns([0.8, 0.2])
   btn = rows[1].button(label='Run Regression Model')
   list_of_features = df.select_dtypes(include=[np.number])
   tab1, tab2, tab3 = st.tabs(["Linear Regression", "Decision Tree Regression", "OLS Regression"])
   features = rows[0].multiselect(label='Search', options=list_of_features.columns[4:])
   target = ['overall_rating']
   df = df.dropna()
   X = df[features]
   y = df[target]
   X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.33,random_state=42)
   if btn:
      with tab1:
         regressor = LinearRegression()
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
      with tab2:
         regressor = DecisionTreeRegressor(max_depth=20)
         regressor.fit(X_train,y_train)
         y_prediction = regressor.predict(X_test)
         st.write(".............Evaluation metrics for Decision Tree Regression..............")
         score = regressor.score(X_test, y_test)
         n=len(df[target])
         p=len(features)
         adjr= 1-(1-score)*(n-1)/(n-p-1)
         st.write("RSquared: ",score)
         st.write("AdjustedRSquared: ",adjr)
         st.write('MAE', metrics.mean_absolute_error(y_test, y_prediction))
         st.write('MSE', metrics.mean_squared_error(y_test, y_prediction))
         st.write('RMSE', np.sqrt(metrics.mean_squared_error(y_test, y_prediction)))
      with tab3:
         #Ordinary Least Squares
         result = sm.OLS(y, X).fit()
         st.write(result.summary())
         


