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
import random


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
data = pickle.load(open("data/Xtrain.p", "rb"))
units = data.index.get_level_values("unit_number").unique()

k = sorted(data.index, key=lambda x: (x[1], random.random()))
data_shuffled = data.loc[k]

#print(data_shuffled.head(3))

#df_indices = data_shuffled.index
#for index, row in data_shuffled.iterrows():
#    new_measurement = row.to_dict()

#print(new_measurement)
#print(df_indices[0: 5])
#print(df_indices[-1])
#for index, row in data_shuffled.loc[unit].iterrows():
#    new_measurement = row.to_dict()

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
pred = np.array([[0]])
chart = st.line_chart(pred)

unit = 58
for index, row in data.loc[unit].iterrows():
    data_len = data.loc[unit].shape[0]
    percent_complete = (index) / data_len
    new_measurement = row.to_dict()
    response = requests.post('http://127.0.0.1:8000/predict', json=new_measurement)
    pred = np.array([[int(response.json()["prediction"])]])
    status_text.text(f"{percent_complete:.2f} Complete")
    chart.add_rows(pred)
    progress_bar.progress(percent_complete)
    #print(pred)
    #b.text(f'unit: {unit}  index: {index}  prediction: {pred}')
    time.sleep(0.05)

# for unit in units:
#     for index, row in data.loc[unit].iterrows():
#         new_measurement = row.to_dict()
#         response = requests.post('http://127.0.0.1:8000/predict', json=new_measurement)
#         pred = np.array([[int(response.json()["prediction"])]])
#         chart.add_rows(pred)
#         #print(pred)
#         #b.text(f'unit: {unit}  index: {index}  prediction: {pred}')
#         time.sleep(0.5)

progress_bar.empty()
st.button("Re-run")

# st.write("Model prediction for remaining useful life")
# b = st.empty()
# while True:
#     for unit in units:
#         for index, row in data_shuffled.loc[unit].iterrows():
#             new_measurement = row.to_dict()
#             response = requests.post('http://127.0.0.1:8000/predict', json=new_measurement)
#             pred = int(response.json()["prediction"])
#             #print(pred)
#             b.text(f'unit: {unit}  index: {index}  prediction: {pred}')
#             time.sleep(0.5)
      