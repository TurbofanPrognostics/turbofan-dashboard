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
from typing import List, Dict
import logging

from html_header import html



# backend request params
port = 80
host = 'turbo-fast-app-dev.us-west-2.elasticbeanstalk.com'
# use this host when testing local FastAPI docker deployment from streamlit
# host = 'host.docker.internal' 
url = f'http://{host}:{port}'

@st.cache
def load_train_data() -> pd.DataFrame:
    """
    load train data for simulation
    """
    train_data = 'train_FD001.feather'
    train_data_file_path = f'data/{train_data}'
    train_df = pd.read_feather(train_data_file_path)

    return train_df

@st.cache
def get_models() -> List[str]:
    response = requests.get(f'{url}/models')
    return response.json()['models']

def pick_model(model_name: str) -> None:
    response = requests.post(f'{url}/select_model', json={'model_name': model_name})
    if response.status_code != 201:
        raise Exception(f'Model Name {model_name} does not exist!')
    logging.info('Model loaded!')

def build_payload(df: pd.DataFrame) -> Dict[str, List[float]]:
    """
    Generates a JSON payload from a loaded pandas dataframe 
    """
    to_return = {}
    df = df.replace({np.nan: 'NaN'})
    df_dict: Dict[str, dict] = df.to_dict()
    for col, inner_dict in df_dict.items():
        to_return[col] = ["NaN" if val == np.nan else val for index, val in inner_dict.items()]
    return to_return

st.set_page_config(page_title="Turbofan Prognostics Dashboard",
                   page_icon="", layout="wide")
st.markdown('<style>body{background-color: #fbfff0}</style>',
            unsafe_allow_html=True)
st.markdown(html, unsafe_allow_html=True)
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """,
unsafe_allow_html=True)

st.title('Hello, my name is TurboFan App!')
st.header('And I like to make engine failure predictions!')

# load test data for simulation
train_df = load_train_data()

# get engines
engines: List[int] = train_df['unit_number'].unique().tolist()

# get models
models: List[str] = get_models()

with st.form(key='simulation_form'):
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    engine_select: int = st.sidebar.selectbox(
                            label="Select Engine #",
                            options=engines,
                            help="Select engine to plot")
    model_select: str = st.sidebar.selectbox(
                            label='Select A Model',
                            options=models,
                            help='Select model for inference')
    submit_button = st.form_submit_button(label='Start Simulation')

    if submit_button:
        # subset training data based on engine selected
        df_ = train_df[train_df['unit_number'] == engine_select]
        df_ = df_.reset_index()
        rul = df_[['RUL']]
        empirical_rul = int(rul.iloc[0])
        df_ = df_.drop(columns=['RUL'])
        placeholder = pd.DataFrame({"empirical_rul": empirical_rul,
                                    "predicted_rul": 125}, index=[0])
        st.subheader(f'Emperical and Predicted remaining useful life '
                     f'for engine # {engine_select}')
        chart = st.line_chart(placeholder)

        # load selected model in backend
        pick_model(model_select)

        # run simulation (different simulation depending on selected model)
        data_len = df_.shape[0]
        percent_complete = 0
        if model_select == 'Baseline Regression Model':
            for index, row in df_.iterrows():
                percent_complete: float = (index + 1) * 1.0 / data_len
                new_measurement = row.to_dict()
                response = requests.post(f'{url}/stream_predict', json=new_measurement)
                pred: int = int(response.json()['prediction'])
                empirical_rul: int = int(rul.iloc[index])
                status_text.text(f"{percent_complete:.2f} Complete")
                chart.add_rows(pd.DataFrame({"empirical_rul": empirical_rul,
                                             "predicted_rul": pred}, index=[index]))
                progress_bar.progress(percent_complete)
                time.sleep(0.05)
        elif model_select == 'Time Series Regression Model':
            payload = build_payload(df_)
            response = requests.post(f'{url}/batch_predict', json=payload)
            predictions = json.loads(response.json()['predictions'])
            
            # run simulation on entire batch of predictions
            for i, pred in enumerate(predictions):
                # first index's prediction will be ignored due to NaNs in lag 1 variables
                index = i + 1
                percent_complete: float = (index + 1) * 1.0 / data_len
                empirical_rul: int = int(rul.iloc[index])
                status_text.text(f"{percent_complete:.2f} Complete")
                chart.add_rows(pd.DataFrame({"empirical_rul": empirical_rul,
                                             "predicted_rul": int(pred)}, index=[index]))
                progress_bar.progress(percent_complete)
                time.sleep(0.05)
