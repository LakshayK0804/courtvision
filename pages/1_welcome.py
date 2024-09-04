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