import pandas as pd
import streamlit as st
import plotly.express as px
import os
import requests
pd.set_option('display.max_columns', None)
import time
import numpy as np




#streamlit - presenting data
st.set_page_config(page_title="CourtSide", page_icon='🏀', layout="wide")
st.title("🏀 CourtSide")
st.markdown('<style>div.block-container{padding-top:3rem;font-family: "montserrat", bold;}</style>', unsafe_allow_html=True)


st.header("Information")
st.caption("This website is for NBA enthusiasts. Wanna find out information about your favourite player? Wanna know how his upcoming season will go? or just a data enthusiast?")
st.caption("You've come to the right place!")
st.caption("Click on the top left to access 'playerdata' or 'visonAI' our insane AI that predicts how your favourite player's upcoming season is gonna go, I can see the gambling enthusiast in you full of joy already :smile")

st.divider()

st.header("About ME")
st.caption("HI, I'm Lakshay Kalra - the creator of this website!")
st.caption("You can find out more about me here")