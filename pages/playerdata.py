import pandas as pd
import streamlit as st
import plotly.express as px
import os
import requests
pd.set_option('display.max_columns', None)
import time
import numpy as np

data = pd.read_excel('../nba-data-scraper/player_data.xlsx')
#Cleaning Data

#data['season_start_year']=['Year'].str[:4].astype(int)
data['TEAM'].replace(to_replace=['NOP','NOH'], value ='NO', inplace=True)
data['Season_type'].replace('Regular%20Season', 'Regular Season', inplace=True)
rs_df = data[data['Season_type']=="Regular Season"]
playoffs_df = data[data['Season_type']=="Playoffs"]

total_cols = ['MIN', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

#Data Analysis
data_per_min = data.groupby(['PLAYER', 'PLAYER_ID', 'Year'])[total_cols].sum().reset_index()
for col in data_per_min.columns[4:]:
    data_per_min[col] = data_per_min[col]/ data_per_min['MIN']

data_per_min['FG%'] = data_per_min['FGM']/data_per_min['FGA']
data_per_min['3PT%'] = data_per_min['FG3M']/data_per_min['FG3A']
data_per_min['FT%'] = data_per_min['FTM']/data_per_min['FTA']
data_per_min['FG3A%'] = data_per_min['FG3A']/data_per_min['FGA']
data_per_min['PTS/FGA'] = data_per_min['PTS']/data_per_min['FGA']
data_per_min['FG3M/FGM'] = data_per_min['FG3M']/data_per_min['FGM']
data_per_min['FTA/FGA'] = data_per_min['FTA']/data_per_min['FGA'] #Free throw attempts per Field Goal Attempt
data_per_min['TRU%'] = 0.5*data_per_min['PTS']/(data_per_min['FGA']+0.475*data_per_min['FTA']) #True shooting percentage - modern measure
data_per_min['AST_TOV'] = data_per_min['AST']/data_per_min['TOV']

#streamlit - presenting data
st.set_page_config(page_title="courtVision", page_icon="🏀", layout="wide")
st.title(" 🏀 statHead")
st.markdown('<style>div.block-container{padding-top:3rem;font-family: "montserrat", bold;}</style>', unsafe_allow_html=True)


#startYear = 2010
#endYear = 2024
#with col1:
    #year1 = pd.to_datetime(st.selectbox("Select Year", range(startYear, endYear)))
st.sidebar.header("Filters: ")
years = st.sidebar.multiselect("Select Year", data['Year'].unique())
if not years:
    df2 = data.copy()
    
else:
    df2 = data[data['Year'].isin(years)]
    
team = st.sidebar.multiselect("Pick your team", df2['TEAM'].unique())
if not team:
    df3 = df2.copy()
else:
    df3 = df2[df2['TEAM'].isin(team)]

players = st.sidebar.multiselect("Select Player", df3['PLAYER'].unique())


if not team and not years and not players:
    filter_df = data
elif not team and not years:
    filter_df = data[data['PLAYER'].isin(players)]
elif not team and not players:
    filter_df = data[data['Year'].isin(years)]
elif not players and not years:
    filter_df = data[data['TEAM'].isin(team)]
elif players and years:
    filter_df = df3[df3['PLAYER'].isin(players) & data['Year'].isin(years)]
elif team and years:
    filter_df = df3[df2['TEAM'].isin(team) & data['Year'].isin(years)]
elif team and players:
    filter_df = df3[df3['PLAYER'].isin(players) & data['Team'].isin(team)]
else:
    filter_df = df3[df3['PLAYER'].isin(players) & df3['TEAM'].isin(team) & df3['Year'].isin(years)]

col1, col2 = st.columns((2))

category_df = filter_df.groupby(['PLAYER', 'PLAYER_ID', 'Year'])[total_cols].sum()
for col in category_df.columns[4:]:
    category_df[col] = category_df[col]/ category_df['MIN']

category_df['FG%'] = category_df['FGM']/category_df['FGA']
category_df['3PT%'] = category_df['FG3M']/category_df['FG3A']
category_df['FT%'] = category_df['FTM']/category_df['FTA']
category_df['FG3A%'] = category_df['FG3A']/category_df['FGA']
category_df['PTS/FGA'] = category_df['PTS']/category_df['FGA']
category_df['FG3M/FGM'] = category_df['FG3M']/category_df['FGM']
category_df['FTA/FGA'] = category_df['FTA']/category_df['FGA'] #Free throw attempts per Field Goal Attempt
category_df['TRU%'] = 0.5*category_df['PTS']/(category_df['FGA']+0.475*category_df['FTA']) #True shooting percentage - modern measure
category_df['AST_TOV'] = category_df['AST']/category_df['TOV']



with col1:
    st.subheader("Shooting Percentage")
    fig = px.bar(category_df, x="FG3M", y = "FG3A", text = ['${:,.2f}'.format(x) for x in category_df['FG3M']],
    template = "seaborn")
    st.plotly_chart(fig,use_container_width=True, height = 200)

with col2:
    st.subheader("Shooting Percentage")
    fig = px.bar(category_df, x="TRU%", y = "FGA", text = ['${:,.2f}'.format(x) for x in category_df['TRU%']],
    template = "seaborn")
    st.plotly_chart(fig,use_container_width=True, height = 200)