import queries.players_stats as queries
import plots.player_plots as plots
import functions
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
from scipy.stats import norm
import io
st.set_page_config(layout="wide")
#Obtain the top-n number of players specified by the field number and the column
def get_top_number_players(number:int, column:str):
    fig = plt.figure(figsize=(10, 5))
    plt.barh(player_attributes["Player"][:number], player_attributes[column][:number], color="#17203b")
    plt.barh(player_attributes["Player"][0], player_attributes[column][0], color="#ff3f34")
    plt.title(f'''Players with the Highest {column} in
    European Football Leagues (2008 ‒ 2016)''')
    plt.xlabel(f"{column} Rating")
    plt.ylabel("Player")
    plt.gca().invert_yaxis()
    return fig
#Obtain the plot of the distribution of the players attributes
def get_plot_of_distribution(df:pd.DataFrame, column:str):
    fig = plt.figure(figsize=(12,8))
    plt.title(column + " Density")
    sns.kdeplot(df, x=column)
    return fig
#Obtain the parameter mu and sigma of the data
def get_distribution_from_data(column:str):
    return norm.fit(player_attributes[column])


st.markdown('# EDA for Players')
st.markdown(''' In this section I'm going to do some basic explainatory data analaysis of the player statistics in order to
            find some interesting characteristics of the data and some correlation between the features. 
            I'm going to start with the display of the dataframe that will be used for the operations, then I'll continue
            to show why I've chosen the features and lastly there are going to be plots of the data.''')

st.markdown('# The dataset')
st.markdown("""In this section we are just going to use two tables: players and players_attributes which respectively 
            describe the anagrafy of the players and the different stats of the player in a specific period.
            The first thing we are going to do is to check the properties of the two datasets.""")
columns = st.columns(2)
st.markdown('## Tables Describtion')
st.markdown('### Player')
st.markdown("""The first table that we are going to investigate is the Player one:""")
players = queries.get_players()
st.dataframe(players.head(),hide_index=True)
st.markdown("""The columns are the following:""")
st.write("""<ul> <li> <b>Player_api_id</b>: id used for identifying a specific player;
            <li> <b>Player_name</b>: name of the player;
            <li> <b>Player_fifa_api_id</b>: id used for identifying the player for the fifa game;
            <li> <b>Birthday</b>: date of birthday of the player;
            <li> <b>Height</b>: height in cm of the player;
            <li> <b>Weight</b>: weight in pounds of the player. </ul>""", unsafe_allow_html=True)
buf = io.StringIO()
players.info(buf=buf)
st.markdown("And if we want to get more information about of the type of the column and the null values")
st.dataframe(functions.get_df_info(buf), hide_index=True)
st.markdown("Lastly let's calculate some ordinary statistics for the height and the weight.")
st.dataframe(players.describe().T[3:])
st.markdown('#### Distributions of player data')
st.markdown('''The first thing that we are going to do is a violin plot which describes the IQR and the distribution of the data.''')
st.pyplot(plots.plot_violin_plot_by_name(players, ['height', 'weight']))
st.markdown('#### Correlation between Height and Weight')

fig = plt.figure(figsize=(15,5))
sns.scatterplot(data=players, x = 'height', y = 'weight')
plt.xlabel('height (cm)')
plt.ylabel('weight (lbs)')
plt.title('Heights and Weights of European Soccer Players')
st.pyplot(fig)

st.markdown('### Player attributes ')
player_attributes = queries.get_players_attributes()
st.dataframe(player_attributes.head(),hide_index=True)
st.markdown(f"""The columns here more than the previous table, more precisely there are a total of {len(player_attributes.columns)} columns.
            The most interesting columns are:
            <ul> 
                <li> <b>Overall_rating</b>: describes the overall rating of the player;
                <li> <b>Potential</b>: indicates the potential of the player;
                <li> <b>Preferred_foot</b>: indicates the preferred foot of the player;
                <li> <b>Others</b>: indicates in a scale of 1-99 how strong that player is in that field;
            </ul>""", unsafe_allow_html=True)
st.markdown('Concerning about the table statistic with respect to the count of the values and of the null ones:')
buf = io.StringIO()
player_attributes.info(buf=buf)
st.dataframe(functions.get_df_info(buf))

st.markdown('We can see that the dataset has over 180k rows, disregarding of the fields which are nulls. A number like this is highly discouraging to work for, because if we see at the computation usage for storing the dataframe:')
st.write('Mega Bytes for storing the frame: ',player_attributes.memory_usage(deep=True).sum() / 1024 / 1024)
st.markdown('''If we display the first five rows of the dataset ordered by the player name, we see something interesting''')
dataframe_with_repetition = queries.get_non_unique_stats()
st.dataframe(dataframe_with_repetition.head(), hide_index=True)
st.markdown("""Those five rows represents five different attributes of the player in five different dates.
            This is because the attributes of the players are obtained by the Fifa game which periodically updates
            the player attributes with respect of their cumulative performance.""")
st.markdown(f"""The total number of rows in the dataset is {dataframe_with_repetition["Player"].size} and the total number of
            different players is {dataframe_with_repetition["Player"].unique().size}. So in average more than
            10 rows for player and if we want to use the data with the pandas library we need a lot of computation power.""")
st.markdown('### Data shrinkage')
st.markdown(f"""We know that using all {dataframe_with_repetition["Player"].size} is a lot and honestly we just don't need
            all those rows for a plyer with we want to get information about it's overall performance between all the season
            that he played. So the idea is to group the data by the player name and then doing the average of all the ratings
            that he got in those years that he played. The resulting dataset is the following""")
players = queries.get_player_stats()
st.dataframe(players[:100], hide_index=True)
st.markdown(f'''Which contains all the information that we need to peform the data analysis. Obviously, using the average of the features
            is not perfectly fine because we're losing some information, but for my purpose this is perfectly fine. Lastly, if we see at the dimension of the dataset''')
st.write('Mega Bytes for storing the frame: ',players.memory_usage(deep=True).sum() / 1024 / 1024, 'which is roughly 300 times smaller than the previous one.')

st.markdown('''## Correlation''')
st.markdown("""The first thing that we're going to do is to determine if some of the features
            of the player are correlated and this is possible by showing the correlation heatmap:""")

plots.plot_correlation_heatmap(players)
st.markdown("""As expected the correlation has a lot of linear correlations and this is motivated by the fact that the features
            can be grouped by 'categories' meaning that some of them are relatively higher on a specific type of player (Striker, Midfielder, Defender, ...)
            and so if one of the features in that category is higher, then the other ones should be too. Another good thing to note is that
            the overall and the potential features are highly correlated to all ones and that is because those two features
            are calculated by the other features.""")
player_attributes= players.sort_values(by="Overall_Rating", ascending=False).reset_index(drop=True)  

st.markdown('''## Preferred foot''')
st.markdown('Another interesting characteristics of the player is the preferred foot, we will start plotting the percentuals of right and left footers and then we would check the distribution of those players.')
foot = queries.get_preferred_foot()
rows = st.columns([0.2, 0.6, 0.2])
fig = plt.figure(figsize=(6, 6))
plt.pie(foot, labels=['Left', 'Right'], autopct='%.0f%%')
rows[1].pyplot(fig)

st.write('As expected there are more right footed players and if we see about the distribution of the players with the respect to the foot then')
left_foot_average = queries.get_ratings_from_foot('left')['avg_rating']
right_foot_average = queries.get_ratings_from_foot('right')['avg_rating']
plots.plot_foot_ratings()
rows = st.columns([0.1, 0.4, 0.4, 0.1])
rows[1].dataframe(right_foot_average.describe().T)
rows[2].dataframe(left_foot_average.describe().T)
st.markdown('''## Strongest players''')

st.markdown("""It may be valuable to find the players that had the highest performance scores (overall ratings) across all seasons
             and leagues during the entire duration to further analyse the correlation between the player attributes
             and how they influenced the performance scores.
             For this reason, I've visualised the top ten players with the highest performance scores (overall ratings) across all
             seasons and leagues during the entire duration as a bar chart.""")

st.pyplot(get_top_number_players(10, "Overall_Rating"))
st.markdown('Another way of seeing this distribution is by plotting the density of the overall ratings:')
st.pyplot(get_plot_of_distribution(player_attributes,'Overall_Rating'))

st.write('''We pretty much see that the distribution seem following a Gaussian one, so we can try to 
        calculate the mean and the variance of the distribution''')
mu, sigma = get_distribution_from_data('Overall_Rating')
st.write(r'$\mu$: ', mu)
st.write(r'$\sigma$: ', sigma)
st.markdown('''There's also another performance measure for players in the database,
             potential, which refers to the upward ceiling of particular player and indicates how high they
             can reach in the attributes. Hence, it could also be useful to find the players that had the highest
             potential across all seasons and leagues during the entire duration to find some relation between
             both performance measures.''')
player_attributes= players.sort_values(by="Potential", ascending=False).reset_index(drop=True) 
st.pyplot(get_top_number_players(10, "Potential"))
st.markdown('''As it stands, Lionel Messi and Cristiano Ronaldo had both the highest overall 
            rating and potential consistently across all seasons and leagues during the entire duration. ''')
st.markdown('''As before, we can try to plot the density function trying to gather more information about the data''')
st.pyplot(get_plot_of_distribution(player_attributes,'Potential'))
mu, sigma = get_distribution_from_data('Potential')
st.write(r'$\mu$: ', mu)
st.write(r'$\sigma$: ', sigma)
st.markdown("""We see that the mean and sigma of the potential and overall_ratings are quite similar and the density function too. So
            with the data that we have till now we can try to do a basic scatter plot using a regression line:""")
fig = plt.figure(figsize=(10,5))
plot = sns.lmplot(x="Potential", y="Overall_Rating", data=player_attributes, scatter_kws={"color": "#ff3f34"}, line_kws={"color": "#7a8092"})
plt.xlabel("Potential")
plt.ylabel("Overall_Rating")
plt.legend(["Data Points", "Regression Line"])
st.pyplot(plot.fig)
