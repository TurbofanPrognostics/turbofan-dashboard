import streamlit as st
import requests
import matplotlib
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pickle
import seaborn as sns
import time


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

# request data
data = pickle.load(open("data/Xtest.p", "rb"))
units = data.index.get_level_values("unit_number").unique()


# new_measurement = {
#     "sensor2": 641.71,
#     "sensor3": 1588.45,
#     "sensor4": 1395.42,
#     "sensor7": 554.85,
#     "sensor8": 2388.01,
#     "sensor9": 9054.42,
#     "sensor11": 47.5,
#     "sensor12": 522.16,
#     "sensor13": 2388.06,
#     "sensor14": 8139.62,
#     "sensor15": 8.3803,
#     "sensor17": 393.0,
#     "sensor20": 39.02,
#     "sensor21": 23.3916,
#     "sensor11_lag_1": 47.2,
#     "sensor12_lag_1": 521.72,
#     "sensor13_lag_1": 2388.03,
#     "sensor14_lag_1": 8125.55,
#     "sensor15_lag_1": 8.4052,
#     "sensor17_lag_1": 392.0,
#     "sensor2_lag_1": 643.02,
#     "sensor20_lag_1": 38.86,
#     "sensor21_lag_1": 23.3735,
#     "sensor3_lag_1": 1585.29,
#     "sensor4_lag_1": 1398.21,
#     "sensor7_lag_1": 553.9,
#     "sensor8_lag_1": 2388.04,
#     "sensor9_lag_1": 9050.17
#     }

st.write("Model prediction for remaining useful life")
b = st.empty()
while True:
    for unit in units:
        for index, row in data.loc[unit].iterrows():
            new_measurement = row.to_dict()
            response = requests.post('http://127.0.0.1:8000/predict', json=new_measurement)
            pred = int(response.json()["prediction"])
            #print(pred)
            b.text(f'{pred}')
            time.sleep(0.5)
      