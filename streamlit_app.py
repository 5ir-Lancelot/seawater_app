import streamlit as st
import os
import numpy as np
import pandas as pd
import PyCO2SYS as pyco2

# Read in the bjerrum plot csv file as lines
lines = pd.read_table('bjerrum_plot.csv', sep=',', keep_default_na=False,
                      na_filter=False, header='infer', engine='python', encoding='utf-8')

# Use the following function when accessing the value of 'my-slider'
# in callbacks to transform the output value to logarithmic
def transform_value(value):
    return 10 ** value

# Set the ranges for the sliders
pH_range = [7.0, 8.5]
pH_step = 0.1

log_fCO2_range = [-4.0, 0.0]
log_fCO2_step = 0.1

T_range = [0.0, 50.0]
T_step = 1.0


TA_range = [1.0,1e+6]
TA_step = 0.1

# Create the interactors
pH_slider = st.slider('pH', pH_range[0], pH_range[1], pH_step,
                      format='%1.1f')
log_fCO2_slider = st.slider('log(fCO2)', log_fCO2_range[0], log_fCO2_range[1], log_fCO2_step,
                             format='%1.1f')

T_slider = st.slider('Temperature (°C)', T_range[0], T_range[1], T_step,
                     format='%1.1f')

TA_slider = st.slider('Alkalininty', TA_range[0], TA_range[1], TA_step,
                     format='%1.1f')

# Set the default values for the interactors
pH_val = 7.8
log_fCO2_val = -3.5
T_val = 25
TA_val = 35

# Calculate the carbonate system parameters
params = pyco2.calc_params(pH=pH_, log_fCO2=log_fCO2_val, T=T_val, S=S_val)

params=pyco2.sys(par1=alkalinity,par2=log_fCO2_slider,par1_type=1,par2_type=4,temperature=T)

# Create the figure
fig = make_subplots(rows=2, cols=2,
                    specs=[[{'type': 'scatter'}, {'type': 'scatter'}],
                           [{'type': 'scatter'}, {'type': 'scatter'}]])

# Add the data to the figure
fig.add_trace(go.Scatter(x=lines['Total Alkalinity'], y=lines['pH'],
                         name='Bjerrum plot',
                         line=dict(color='blue', width=1)),
              row=1, col=1)
fig.add_trace(go.Scatter(x=[params['TA']], y=[params['pHin']],
                         name='input',
                         marker=dict(color='red'),
                         text=['TA: ' + str(params['TA']) + '<br>pH']))

