import pandas as pd
import streamlit as st
import plotly.express as px
import os
import requests
pd.set_option('display.max_columns', None)
import time
import numpy as np
from nba_api.stats.endpoints import playergamelog
from nba_api.live.nba.endpoints import scoreboard

games = scoreboard.ScoreBoard()
games.get_json()
games.get_dict()
data = pd.read_excel('./player_data.xlsx')
#Cleaning Data

#data['season_start_year']=['Year'].str[:4].astype(int)
data['TEAM'].replace(to_replace=['NOP','NOH'], value ='NO', inplace=True)
data['Season_type'].replace('Regular%20Season', 'Regular Season', inplace=True)
rs_df = data[data['Season_type']=="Regular Season"]
playoffs_df = data[data['Season_type']=="Playoffs"]

total_cols = ['MIN', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']



#streamlit - presenting data
st.set_page_config(page_title="CourtSide", page_icon='🏀', layout="wide")
st.title("🏀 CourtSide")
st.markdown('<style>div.block-container{padding-top:3rem;font-family: "montserrat", bold;}</style>', unsafe_allow_html=True)


#startYear = 2010
#endYear = 2024
#with col1:
    #year1 = pd.to_datetime(st.selectbox("Select Year", range(startYear, endYear)))
