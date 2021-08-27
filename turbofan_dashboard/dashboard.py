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


print('Haggu')

# # request data
# data = pickle.load(open("data/Xtrain.p", "rb"))
# training_ruls = pickle.load(open("data/ytrain.p", "rb"))
# training_ruls.rename("predicted_rul")
# units = data.index.get_level_values("unit_number").unique()

# # Shuffle rows for simulated evolution of units operating cycles
# def sim_operation(df):
#     T = list(df.index)
#     groups = {g:iter([t for t in T if t[0]==g]) for g in dict(T)}
#     sim_idx = [next(groups[v0]) for v0,_ in sample(T,len(T))]
#     return data.loc[sim_idx]

# #data_shuffled = sim_operation(data)

# progress_bar = st.sidebar.progress(0)
# status_text = st.sidebar.empty()
# unit_selector = st.sidebar.selectbox(label="Unit Number",
#                                       options = units,
#                                       help="Select unit number to plot",
#                                       index = 1
#                                       )

# placeholder = pd.DataFrame({"empirical_rul": 125, "predicted_rul": 125}, index=[0])
# unit = unit_selector

# st.subheader(f'Emperical and Predicted remaining useful life for unit {unit}')
# chart = st.line_chart(placeholder)

# for index, row in data.loc[unit].iterrows():
#     data_len = data.loc[unit].shape[0] + 1
#     percent_complete = (index) / data_len
#     new_measurement = row.to_dict()
#     response = requests.post('http://127.0.0.1:8000/predict', json=new_measurement)
#     pred = int(response.json()["prediction"])
#     emp_rul = training_ruls.loc[unit][index]
#     status_text.text(f"{percent_complete:.2f} Complete")
#     chart.add_rows(pd.DataFrame({"empirical_rul": emp_rul, "predicted_rul": pred}, index=[index]))
#     progress_bar.progress(percent_complete)
#     #b.text(f'unit: {unit}  index: {index}  prediction: {pred}')
#     time.sleep(0.05)


# progress_bar.empty()      
