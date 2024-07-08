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
st.set_page_config(page_title="courtVision", page_icon=":basketball:", layout="wide")
st.title(" :basketball: courtVision")
st.markdown('<style>div.block-container{padding-top:3rem;font-family: "montserrat", bold;}</style>', unsafe_allow_html=True)


#startYear = 2010
#endYear = 2024
#with col1:
    #year1 = pd.to_datetime(st.selectbox("Select Year", range(startYear, endYear)))

