import streamlit as st
import requests
import matplotlib
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pickle
import seaborn as sns
import time
import numpy as np
import pandas as pd
import random
from random import sample
import json
from typing import List


@st.cache
def load_train_data() -> pd.DataFrame:
    """
    load train data for simulation
    """
    train_data = 'train_FD001.feather'
    train_data_file_path = f'data/{train_data}'
    train_df = pd.read_feather(train_data_file_path)

    return train_df


html_header="""
<head>
<title>Predictive Maintenance</title>
<meta charset="utf-8">
<meta name="keywords" content="turbofan prognostics, dashboard, predictive maintenance">
<meta name="description" content="turbofan prognostic dashboard">
<meta name="author" content="Team prognostics">
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<h1 style="font-size:300%; color:#008080; font-family:Georgia"> Turbofan Prognostics <br>
 <h2 style="color:#008080; font-family:Georgia"> DASHBOARD</h3> <br>
 <hr style= "  display: block;
  margin-top: 0.5em;
  margin-bottom: 0.5em;
  margin-left: auto;
  margin-right: auto;
  border-style: inset;
  border-width: 1.5px;"></h1>
"""

st.set_page_config(page_title="Turbofan Prognostics Dashboard", page_icon="", layout="wide")
st.markdown('<style>body{background-color: #fbfff0}</style>',unsafe_allow_html=True)
st.markdown(html_header, unsafe_allow_html=True)
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

# backend request params
port = 80
host = 'turbo-fast-app-dev.us-west-2.elasticbeanstalk.com'
# use this host when testing local FastAPI docker deployment from streamlit
# host = 'host.docker.internal' 
url = f'http://{host}:{port}/stream_predict'

st.title('Hello, my name is TurboFan App!')
st.header('And I like to make engine failure predictions!')

# load test data for simulation
train_df = load_train_data()

# get engines
engines: List[int] = train_df['unit_number'].unique().tolist()

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
engine_select: int = st.sidebar.selectbox(
                        label="Engine #",
                        options=engines,
                        help="Select engine to plot")

# subset training data based on engine selected
df_ = train_df[train_df['unit_number'] == engine_select]
df_ = df_.reset_index()
rul = df_[['RUL']]
empirical_rul = int(rul.iloc[0])
df_ = df_.drop(columns=['RUL'])
placeholder = pd.DataFrame({"empirical_rul": empirical_rul, "predicted_rul": 125}, index=[0])
st.subheader(f'Emperical and Predicted remaining useful life for engine # {engine_select}')
chart = st.line_chart(placeholder)

# run simulation
data_len = df_.shape[0]
percent_complete = 0
for index, row in df_.iterrows():
    percent_complete = (index + 1) * 1.0 / data_len
    new_measurement = row.to_dict()
    response = requests.post(url, json=new_measurement)
    pred: int = int(response.json()['prediction'])
    empirical_rul: int = int(rul.iloc[index])
    status_text.text(f"{percent_complete:.2f} Complete")
    chart.add_rows(pd.DataFrame({"empirical_rul": empirical_rul, "predicted_rul": pred}, index=[index]))
    progress_bar.progress(percent_complete)
    time.sleep(0.05)
