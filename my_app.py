# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 14:05:38 2021

@author: watda

my app should be tidied up and inspired by Chris one


run it to test it on the local browser

python my_app.py
"""
import os
import flask
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_defer_js_import as dji
import numpy as np

from plotly.subplots import make_subplots

import pandas as pd


# import the package for calculating everything
import PyCO2SYS as pyco2

#from components import solve

external_stylesheets = ['https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css',
                        'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.18.1/styles/monokai-sublime.min.css']

#external_stylesheets=[dbc.themes.CYBORG]


external_scripts = ['https://code.jquery.com/jquery-3.2.1.slim.min.js',
                    'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js',
                    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js']

# Server definition

server = flask.Flask(__name__)

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                external_scripts=external_scripts,
                server=server)

# title that will be visible in the browser tab
app.title = 'Seawater Open Carbonate System Alkalinity Calculations'

# for Heroku to regognize it
server=app.server

filepath = os.path.split(os.path.realpath(__file__))[0]
narrative_text = open(os.path.join(filepath, "narrative.md"), "r").read()
refs_text = open(os.path.join(filepath, "references.md"), "r").read()
some_text = open(os.path.join(filepath, "sometext.md"), "r").read()

mathjax_script = dji.Import(src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/latest.js?config=TeX-AMS-MML_SVG")

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            <script type="text/x-mathjax-config">
            MathJax.Hub.Config({
                tex2jax: {
                inlineMath: [ ['$','$'],],
                processEscapes: true
                }
            });
            </script>
            {%renderer%}
        </footer>
    </body>
</html>
'''

# COMPONENTS
# ==========

# read in the bjerrum plot csv file as lines
lines=pd.read_table('bjerrum_plot.csv',sep=',', keep_default_na=False\
                    , na_filter=False, header='infer',engine='python', encoding='utf-8')


# Use the following function when accessing the value of 'my-slider'
# in callbacks to transform the output value to logarithmic
def transform_value(value):
    return 10 ** value



## Interactors
## -----------

#set the ranges for the sliders
T_range=[0,80]
CO2_range=[200,1000]
alkalinity_range=[1,1e+6]

T_slider=dcc.Slider(id='T_input', min=T_range[0], max=T_range[1], step=0.5, marks={x: str(x)+'°C' for x in range(T_range[0],T_range[1],10)},
        value=5, tooltip={"placement": "bottom", "always_visible": True}, updatemode='drag')

CO2_slider=dcc.Slider(id='CO2_input', min=CO2_range[0], max=CO2_range[1], step=10, marks={x: str(x)+'ppm' for x in range(CO2_range[0],CO2_range[1],100)},
        value=415, tooltip={"placement": "bottom", "always_visible": True}, updatemode='drag')

alkalinity_slider=dcc.Slider(id='alkalinity_input', min=np.log10(alkalinity_range[0]) ,max=np.log10(alkalinity_range[1]), step=0.01,
        marks={x: '{:.0e}'.format(10**x)+' ueq/L' for x in range(0,6,int(1))},value=np.log10(2500),
        tooltip={"placement": "bottom", "always_visible": True},
        updatemode='drag',drag_value=3)


# APP LAYOUT
# ==========

app.layout = html.Div([
    dbc.Container(children=[
        dcc.Markdown(narrative_text, dangerously_allow_html=True),
        
        #dcc.Graph(id="sir_solution", figure=display_SIR_solution(solve(delta=0.5, R0=2.67, tau=8.5))),
        
        dbc.Row(children=[dbc.Col(children=["water tempearture [°C]:"], className="col-md-4"),
                          dbc.Col(children=[T_slider], className="col-md-8")]),
        html.Br(),
        dbc.Row(children=[dbc.Col(children=["Ambient air CO2 partial pressure [ppm]:"], className="col-md-4"),
                          dbc.Col(children=[CO2_slider], className="col-md-8")]),
        html.Br(),
        dbc.Row(children=[dbc.Col(children=["Total Alkalinity [ueq/L]:"], className="col-md-4"),
                          dbc.Col(children=[alkalinity_slider], className="col-md-8")]),
        html.Br(),
        html.Br(),
        dcc.Graph(id='indicator-graphic'),
        dcc.Markdown(some_text, dangerously_allow_html=True),
        html.Br(),
        dcc.Markdown(refs_text, dangerously_allow_html=True)
    ]),
    mathjax_script
])


# INTERACTION
# ===========

@app.callback(Output("indicator-graphic", "figure"),
              [Input("T_input", "value"),
               Input("CO2_input", "value"),
               Input("alkalinity_input", "value")])





def update_graph(T,CO2,alkalinity):
    
    
    # because of the log10 scale of the alkalinity slider
    alkalinity=10**alkalinity
    #https://plotly.com/python/subplots/
    
    #https://plotly.com/python/bar-charts/
    
    #data=dissolution(pH,T,CO2)
    
    # the pyCO2 function is made for ocean carbonate system and will give back 
    # a bunch of different parameters
    
    # https://pyco2sys.readthedocs.io/en/latest/co2sys_nd/
    
    '''
    Carbonate system parameters¶

Either two, one or no carbonate system parameters can be provided.

    par1 and par2: values of two different carbonate system parameters.
    par1_type and par2_type: which types of parameter par1 and par2 are.

If two parameters are provided, these can be any pair of:

    Total alkalinity (type 1) in μmol·kg−1.
    Dissolved inorganic carbon (type 2) in μmol·kg−1.
    pH (type 3) on the Total, Seawater, Free or NBS scale1. Which scale is given by the argument opt_pH_scale.
    Any one of:
        Partial pressure of CO2 (type 4) in μatm,
        Fugacity of CO2 (type 5) in μatm,
        Aqueous CO2 (type 8) in μmol·kg−1, or
        Dry mole fraction of CO2 (type 9) in ppm.
    Carbonate ion (type 6) in μmol·kg−1.
    Bicarbonate ion (type 7) in μmol·kg−1.

    '''
    data=pyco2.sys(par1=alkalinity,par2=CO2,par1_type=1,par2_type=4,temperature=T)
    
    
    # for the pH dependant plot (whole pH range)
    
    
    # take the interesting parameters from the dict output 
   
    
    #to just get the variable names cretae a list
    keys=list(data.keys())
    values=list(data.values())
    
    #atach numbers to them
    
    
    #index of the interesting varibles i wnat to use
    idx=[5,63,64,65]
    
    x_bar=[keys[item] for item in idx]
    y_bar=[values[item] for item in idx]
    
    
    
    
    #plotly command for plots
    # very simple plot that already works 
    #fig= px.line(x=np.linspace(0, 10, 1000),y=T*np.linspace(0, 10, 1000))
    
    #line break in plotly strings <br>
    
    #marker_color defines the different bar colors (it can be also dependent on paramameters, continiuos or distinct)
    # the numbers refer to different colors ( I dont know the exact colors)
    
    fig = make_subplots(rows=1, cols=3, subplot_titles=('Inorganic carbon components <br> in ocean water','DIC(T,CO2_atm,pH)',
                                                        "Fractions of <br> DIC(T,CO2_atm,pH)"),column_widths=[0.3, 0.2, 0.5])
    
    # all possible layout settings
    # https://plotly.com/python/reference/layout/
    
    fig.update_layout(
            font_family="Courier New",
            font_size=20,
            font_color="black",
            title_font_family="Courier New",
            title_font_size=29,
            title_font_color="red",
            legend_title_font_color="green",
            height=800, # global plot height
            width=1700,
            title_text="Equilibrium Solution for Seawater"
            
            )
    
   
    
    
    
    #
    x_bar=['DIC',r'$HCO_{3_{aq}}^{-1}$','$CO_{3_{aq}}^{-2}$','$CO_{2_{aq}}$']
    
    water_type=['seawater']  # here one can add freshwater etc if it would be interesting in this case
    
    fig.add_trace(go.Bar(name=x_bar[3], x=water_type, y=[y_bar[3]]),row=1, col=1) 
    
    fig.add_trace(go.Bar(name=x_bar[1], x=water_type, y=[y_bar[1]]),row=1, col=1)
    
    fig.add_trace(go.Bar(name=x_bar[2], x=water_type, y=[y_bar[2]]),row=1, col=1)
              
   
    
    # Change the bar mode
    fig.update_layout(barmode='stack')
    
    #to see the very big differences I use a logarithmic scale
    # Update xaxis properties  for just the first plot
    fig.update_yaxes(title_text="concentration [umol/L]", row=1, col=1)
    
    # attention range is in log so 10^0  to 10^6
    
    
    
    
     # DIC 
    fig.add_trace(go.Bar(name=x_bar[0], x=['DIC'], y=[y_bar[0]]),row=1, col=2) 
    fig.update_yaxes(range=[0,10000],row=1, col=2)
   
    
    
   
   # input is the array and then it is defined which columns are x and y
   
    fig.add_trace(go.Scatter(x=lines['pH'],y=lines['CO2_frac'],  mode='lines+markers',name='CO2aq' ),row=1, col=3)
    fig.add_trace(go.Scatter(x=lines['pH'],y=lines['HCO3_frac'], mode='lines+markers',name='HCO3aq' ),row=1, col=3)
    fig.add_trace(go.Scatter(x=lines['pH'],y=lines['CO3_frac'], mode='lines+markers',name='CO3aq'),row=1, col=3)
    
    
    fig.update_yaxes(title_text="Fraction in decimal ",title_standoff =4, ticksuffix='', row=1, col=3)
    
    fig.update_xaxes(title_text="pH", row=1, col=3)
    
    pH=data['pH']
    

    
    # Add shapes
    fig.update_layout(
            shapes=[
                    #draw a shape in the third plot   
                    #the reference is the second xref yref
                    dict(type="line", xref="x3", yref='y3',
                              x0=pH, y0=0, x1=pH, y1=1),])
    
    fig.add_annotation(x=12, y=0.7,
            text="pH={:.2f}".format(pH),
            showarrow=False,
            yshift=1,row=1, col=3)
    
    
    #fig.update_layout(height=600, width=800, title_text=r"$\alpha Simulation of Dissolved Carbon Dioxide <br> (assume open system in equilibrium) <br> <br>$")

    #it is not possible to add latex in interactive dash


    return fig
# =============================================================================
# 
# def update_plot(r0_input, delta_input, tau_input):
#     return display_SIR_solution(solve(delta=delta_input, R0=r0_input, tau=tau_input))
# =============================================================================


if __name__ == '__main__':
    app.run_server(debug=True)
