import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import os
import requests
pd.set_option('display.max_columns', None)
import time
import numpy as np
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players


data = pd.read_excel('./player_data.xlsx')
#Cleaning Data
data['season_start_year'] = data['Year'].str[:4].astype(int)
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
data_per_min = data_per_min[data_per_min['MIN']>=50]
data_per_min.drop(columns='PLAYER_ID', inplace=True)

#streamlit - presenting data
st.set_page_config(page_title="CourtSide", page_icon="🏀", layout="wide")
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

players_var = st.sidebar.multiselect("Select Player", df3['PLAYER'].unique())


if not team and not years and not players_var:
    filter_df = data
elif not team and not years:
    filter_df = data[data['PLAYER'].isin(players_var)]
elif not team and not players_var:
    filter_df = data[data['Year'].isin(years)]
elif not players_var and not years:
    filter_df = data[data['TEAM'].isin(team)]
elif players_var and years:
    filter_df = df3[df3['PLAYER'].isin(players_var) & data['Year'].isin(years)]
elif team and years:
    filter_df = df3[df2['TEAM'].isin(team) & data['Year'].isin(years)]
elif team and players_var:
    filter_df = df3[df3['PLAYER'].isin(players_var) & data['TEAM'].isin(team)]
else:
    filter_df = df3[df3['PLAYER'].isin(players_var) & df3['TEAM'].isin(team) & df3['Year'].isin(years)]



category_df = filter_df.groupby(['PLAYER', 'Year'])[total_cols].sum()
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



change_df = data.groupby('season_start_year')[total_cols].sum().reset_index()
change_df['POSS_est'] = change_df['FGA']-change_df['OREB']+change_df['TOV']+0.44*change_df['FTA']
change_df = change_df[list(change_df.columns[0:2])+['POSS_est']+list(change_df.columns[2:-1])]

change_df['FG%'] = change_df['FGM']/change_df['FGA']
change_df['3PT%'] = 100*change_df['FG3M']/change_df['FG3A']
change_df['FT%'] = 100*change_df['FTM']/change_df['FTA']
change_df['AST%'] = change_df['AST']/change_df['FGM']
change_df['FG3A%'] = 100*change_df['FG3A']/change_df['FGA']
change_df['FG3M%'] = 100*change_df['FG3M']/change_df['FGM']
change_df['PTS/FGA'] = change_df['PTS']/change_df['FGA']
change_df['FG3M/FGM'] = change_df['FG3M']/change_df['FGM']
change_df['FTA/FGA'] = change_df['FTA']/change_df['FGA']
change_df['TRU%'] = 0.5*change_df['PTS']/(change_df['FGA']+0.475*change_df['FTA'])
change_df['AST_TOV'] = change_df['AST']/change_df['TOV']

def gen_stats():

    change_per100_df = change_df.copy()

    for col in change_per100_df.columns[3:18]:
        change_per100_df[col] = (change_per100_df[col]/change_per100_df['POSS_est'])*100

    change_per100_df.drop(columns=['MIN','POSS_est'], inplace=True)

    fig_3p = go.Figure()
    fig_3p.add_trace(go.Scatter(x=change_per100_df['season_start_year'],
                                y=change_per100_df['FG3A%'], name="Attempts"))
    fig_3p.add_trace(go.Scatter(x=change_per100_df['season_start_year'],
    y=change_per100_df['FG3M%'], name="Makes"))
    fig_3p.add_trace(go.Scatter(x=change_per100_df['season_start_year'],
    y=change_per100_df['3PT%'], name="3P Shooting Percentage"))
    #for col in change_per100_df.columns[1:]:
    #    fig_3p.add_trace(go.Scatter(x=change_per100_df['season_start_year'],
    #                             y=change_per100_df['FG3A'], name=col))
    fig_FT = go.Figure()
    fig_FT.add_trace(go.Scatter(x=change_per100_df['season_start_year'],
                                y=change_per100_df['FTA'], name="Attempts"))
    fig_FT.add_trace(go.Scatter(x=change_per100_df['season_start_year'],
    y=change_per100_df['FTM'], name="Makes"))
    fig_FT.add_trace(go.Scatter(x=change_per100_df['season_start_year'],
    y=change_per100_df['FT%'], name="FT %"))

    fig_PF = go.Figure()

    fig_PF.add_trace(go.Scatter(x=change_per100_df['season_start_year'],
                                y=change_per100_df['PF'], name="Fouls"))

    fig_RB = go.Figure()

    fig_RB.add_trace(go.Scatter(x=change_per100_df['season_start_year'],
                                y=change_per100_df['OREB'], name="Offensive REB"))
    fig_RB.add_trace(go.Scatter(x=change_per100_df['season_start_year'],
                                y=change_per100_df['DREB'], name="Defensive REB"))
        
    st.divider()

    
    st.header('Has the NBA changed?')
    st.caption('*each statistic is shown based on every 100 possesions from 2010.')
    st.caption('*you can isolate each trace on the graph by clicking the key on the side. ')
    st.subheader('3 point shooting:')
    st.plotly_chart(fig_3p)
    st.subheader('Free throws: ')
    st.plotly_chart(fig_FT)
    st.subheader("Fouls:")
    st.plotly_chart(fig_PF)
    st.subheader('Rebounding:')
    st.plotly_chart(fig_RB)

team_flag = False
st.header("Information")
if not team and not years and not players_var:
    st.text("View overall stats about your favourite league or select filters from the sidebar to view specific stats about your favourite player")
    gen_stats()
elif not team and not years:
    st.text(f"Name: {players_var[0]}")
elif not team and not players_var:
    st.text(f"Year: {years[0]}")
elif not players_var and not years:
    st.text(f"Team: {team[0]}")
    team_flag = True
elif players_var and years:
    st.text(f"Name: {players_var[0]}")
    st.text(f"Year: {years[0]}")
elif team and years:
    st.text(f"Team: {team[0]}")
    st.text(f"Year: {years[0]}")
    team_flag = True
elif team and players_var:
    st.text(f"Name: {players_var[0]}")
    st.text(f"Team: {team[0]}")
    team_flag = True
else:
    st.text(f"Name: {players_var[0]}")
    st.text(f"Team: {team[0]}")
    st.text(f"Year: {years[0]}")
    team_flag = True

#def print_stats(ps_teamupdate):

#def player_stats(players_var):


try:
    st.text(f"{players_var[0]}")
    nba_players = players.get_players()
    player_id = [player for player in nba_players if player['full_name'] == players_var[0]][0]
    player_id = player_id['id']
    career = playercareerstats.PlayerCareerStats(player_id=f"{player_id}")
    playerstats_df = career.get_data_frames()[0]
    playerstats_df.drop(columns=['PLAYER_ID','LEAGUE_ID','TEAM_ID'], inplace=True)
    playerstats_df['SEASON_ID'] = playerstats_df['SEASON_ID'].str[:4].astype(int)
    player_df = playerstats_df.copy()


    change_player_100 = player_df.copy()
    player_FG = go.Figure()

    player_FG.add_trace(go.Scatter(x=change_player_100['SEASON_ID'],
                                y=change_player_100['FGA'], name="Fouls"))
    player_FG.add_trace(go.Scatter(x=change_player_100['SEASON_ID'],
                                y=change_player_100['FGM'], name="Offensive REB"))
    player_FG.add_trace(go.Scatter(x=change_player_100['SEASON_ID'],
                                y=change_player_100['FG_PCT'], name="Offensive REB"))
    player_3p = go.Figure()
    player_3p.add_trace(go.Scatter(x=change_player_100['SEASON_ID'],
                                y=change_player_100['FG3A'], name="Attempts"))
    player_3p.add_trace(go.Scatter(x=change_player_100['SEASON_ID'],
    y=change_player_100['FG3M'], name="Makes"))
    player_3p.add_trace(go.Scatter(x=change_player_100['SEASON_ID'],
    y=change_player_100['FG3_PCT']*100, name="3P Shooting Percentage"))
    #for col in change_player_100.columns[1:]:
    #    fig_3p.add_trace(go.Scatter(x=change_player_100['SEASON_ID'],
    #                             y=change_player_100['FG3A'], name=col))
    player_FT = go.Figure()
    player_FT.add_trace(go.Scatter(x=change_player_100['SEASON_ID'],
                                y=change_player_100['FTA'], name="Attempts"))
    player_FT.add_trace(go.Scatter(x=change_player_100['SEASON_ID'],
    y=change_player_100['FTM'], name="Makes"))
    player_FT.add_trace(go.Scatter(x=change_player_100['SEASON_ID'],
    y=change_player_100['FT_PCT']*100, name="FT %"))

    player_FG = go.Figure()

    player_FG.add_trace(go.Scatter(x=change_player_100['SEASON_ID'],
                                y=change_player_100['FGA'], name="Attempts"))
    player_FG.add_trace(go.Scatter(x=change_player_100['SEASON_ID'],
                                y=change_player_100['FGM'], name="Makes"))
    player_FG.add_trace(go.Scatter(x=change_player_100['SEASON_ID'],
                                y=change_player_100['FG_PCT']*100, name="FG Percentage"))
    fig_RB = go.Figure()

    fig_RB.add_trace(go.Scatter(x=change_player_100['SEASON_ID'],
                                y=change_player_100['OREB'], name="Offensive REB"))
    fig_RB.add_trace(go.Scatter(x=change_player_100['SEASON_ID'],
                                y=change_player_100['DREB'], name="Defensive REB"))
        
    st.divider()
    st.plotly_chart(player_3p)
    st.plotly_chart(player_FG)
    st.plotly_chart(player_FT)
    if team_flag == True:
        tm_name = team[0]
        ps_teamupdate = playerstats_df[playerstats_df['TEAM_ABBREVIATION']==tm_name]

except IndexError:
    st.text("Please select a player!")
    pass

#playerstats_df

#player_stats(players_var)
