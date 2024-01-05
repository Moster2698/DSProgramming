import pandas as pd
import streamlit as st
import numpy as np
import io
from plots import player_plots 
import queries.players_stats as queries
from sklearn.linear_model import LinearRegression
from sklearn import datasets, ensemble
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
import functions as funct
st.set_page_config(layout="wide")
st.markdown('# Regression')
st.markdown('Regression is a statistical method used to analyze the relationship between one or more independent variables and a dependent variable. It is a powerful tool in the field of data analysis and machine learning, providing insights into the patterns and trends within datasets.')
st.markdown('## What you can do in this page')
st.markdown('The focus of this page is to do different types of regression for the player_attributes table on the dependent variable *overall_rating*. In this page you can also choose between three different types of regression: Linear, DecisionTree or OLS.')
st.markdown('## Dataset')
st.markdown('The dataset that we are going to use is the player attributes table')

df = queries.get_players_attributes()
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
if df is not None:
   st.dataframe(df.head())
   st.markdown('If we look the info of the database we note that not all the columns are useful for the regression:')
   buf = io.StringIO()
   df.info(buf = buf )
   st.dataframe(funct.get_df_info(buf)) 
   st.markdown('## Data cleaning')
   st.markdown('The following thing to do is dropping the useless columns which comprehends ids, preferred_foots and birth date. We will only focus on the stats of players which are numerics.')
   list_of_features = df.select_dtypes(include=[np.number])
   list_of_features.drop(labels=['id', 'player_fifa_api_id', 'player_api_id'],axis=1, inplace=True)
   st.write(list_of_features.columns)
   st.markdown('## Correlation')
   st.markdown('''The next thing to do is trying to get some more information about the linearity of the attributes. As done in the
               player stats page, we are going to show a correlation heatmap, but in this case we are only interested
               in the overall_rating column. So we will not get a matrix, but only a single column sorted by the coefficient: ''')
   player_plots.plot_correlation_heatmap_overall(df[list_of_features.columns])
   form = st.form('input_form', border=False)
   rows = form.columns([0.7, 0.3])
   features = rows[0].multiselect(label='Select Features', options=list_of_features.columns[1:])
   rows[1].write('')
   rows[1].write('')
   submitted = rows[1].form_submit_button("Run Regression Model")
   second_form = rows[0].columns([0.33, 0.33, 0.34])
   estimators = second_form[0].slider(label='Number of Estimators', min_value=1, max_value=500, value=250)
   max_depth = second_form[1].slider(label='Max Depth', min_value=1, max_value=20, value=5, step=1)
   learning_rate = second_form[2].slider(label='Learning rate ', min_value=0.0, max_value=1.00, value=0.01, step=0.01)
   loss = rows[1].selectbox(label='Loss function', options=['squared_error', 'absolute_error', 'huber', 'quantile'])
   rows = st.columns([0.8, 0.2])
   if submitted:
      target = ['overall_rating']
      df = df.dropna()
      X = df[features]
      y = df[target]
      X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.11,random_state=42)
      params = {
      "n_estimators": estimators,
      "max_depth": max_depth,
      "learning_rate": learning_rate,
      "loss": loss,
      }
      reg = ensemble.GradientBoostingRegressor(**params)
      reg.fit(X_train, y_train)
      mse = mean_squared_error(y_test, reg.predict(X_test))
      st.write("The mean squared error (MSE) on test set: {:.4f}".format(mse))
      test_score = np.zeros((params["n_estimators"],), dtype=np.float64)
      for i, y_pred in enumerate(reg.staged_predict(X_test)):
         test_score[i] = mean_squared_error(y_test, y_pred)

      fig = plt.figure(figsize=(6, 6))
      plt.subplot(1, 1, 1)
      plt.title("Deviance")
      plt.plot(
         np.arange(params["n_estimators"]) + 1,
         reg.train_score_,
         "b-",
         label="Training Set Deviance",
      )
      plt.plot(
         np.arange(params["n_estimators"]) + 1, test_score, "r-", label="Test Set Deviance"
      )
      plt.legend(loc="upper right")
      plt.xlabel("Boosting Iterations")
      plt.ylabel("Deviance")
      fig.tight_layout()
      st.pyplot(fig)
      feature_importance = reg.feature_importances_
      sorted_idx = np.argsort(feature_importance)
      pos = np.arange(sorted_idx.shape[0]) + 0.5

      fig = plt.figure(figsize=(12, 6))
      plt.subplot(2, 1, 1)
      plt.barh(pos, feature_importance[sorted_idx], align="center")
      plt.yticks(pos, np.array(features)[sorted_idx])
      plt.title("Feature Importance (MDI)")

      result = permutation_importance(
         reg, X_test, y_test, n_repeats=10, random_state=42, n_jobs=2
      )
      sorted_idx = result.importances_mean.argsort()
      plt.subplot(2, 1, 2)
      plt.boxplot(
         result.importances[sorted_idx].T,
         vert=False,
         labels=np.array(features)[sorted_idx],
      )
      plt.title("Permutation Importance (test set)")
      fig.tight_layout()
      st.pyplot(fig)