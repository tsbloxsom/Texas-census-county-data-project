# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

import plotly.express as px
from urllib.request import urlopen
import json

import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#F0F8FF',
    'text': '#00008B'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv("time_series_plotly.csv")

fig = px.scatter(df, x='Date', y='Case Count', color='County')

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

df2 = pd.read_csv("geo_cases_plotly.csv")

df3 = pd.read_csv("bubble_geo_cases_plotly.csv")

cities_for_map = pd.read_csv("cities_for_geo_map.csv")

max_cases = df2["Cases per 100000 population"].max()

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
    
fig2 = px.choropleth(df2, geojson=counties, locations='FIPS #', color='Cases per 100000 population',
                           color_continuous_scale="Reds",
                           hover_name = "County Name",
                           range_color=(0, max_cases),
                           scope = "usa",
                           title = "Cases per 100000 population over past 7 days",
                           labels={"FIPS #": "FIPS", "Cases per 100000 population": "Cases per 100000 pop"}
                          )
    
fig2.update_layout(title_text='Cases per 100000 population over past 7 days', title_x=0.5)

# to show texas cities on map
fig2.add_trace(go.Scattergeo(
    locationmode = 'USA-states',
    lon = cities_for_map['lng'],
    lat = cities_for_map['lat'],
    hoverinfo = 'text',
    text = cities_for_map['city'],
    mode = 'markers',
    marker = dict(
        size = 4,
        color = 'rgb(102,102,102)',
        line = dict(
            width = 3,
            color = 'rgba(68, 68, 68, 0)'
        )
    )))

fig2.update_geos(fitbounds="locations")
fig2.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig3 = px.choropleth(df3, geojson=counties, locations='FIPS #',
                           hover_name = "County",
                           scope = "usa",
                           title = "Total Cases",
                          )

colors_fig3 = ['rgb(189,215,231)','rgb(107,174,214)','rgb(33,113,181)','rgb(239,243,255)']
months = {5: 'May', 6:'June',7:'July',8:'Aug'}

#plot each bubble month cases for each county
for i in range(5,9)[::-1]:
    mask = df3["month"] == i
    df_month = df3[mask]
    #print(df_month)
    fig3.add_trace(go.Scattergeo(
            locationmode = 'USA-states',
            lon = df_month['X (Lat)'],
            lat = df_month['Y (Long)'],
            text = df_month[['County','Case Count']],
            name = months[i],
            mode = 'markers',
            marker = dict(
                size = df_month['Case Count'],
                color = colors_fig3[i-6],
                line_width = 0,
                sizeref = 9,
                sizemode = "area",
                reversescale = True
            )))
    
# to show texas cities on map
fig3.add_trace(go.Scattergeo(
    locationmode = 'USA-states',
    lon = cities_for_map['lng'],
    lat = cities_for_map['lat'],
    hoverinfo = 'text',
    text = cities_for_map['city'],
    name = "Major Cities",
    mode = 'markers',
    marker = dict(
        size = 4,
        color = 'rgb(102,102,102)',
        line = dict(
            width = 3,
            color = 'rgba(68, 68, 68, 0)'
        )
    )))

fig3.update_geos(fitbounds="locations")
fig3.update_layout(title_text='Total Cases per month for last 4 months', title_x=0.5)

fig3.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

markdown_text = '''
### Texas COVID-19 Dashboard

Creator: Truett Bloxsom, [LinkedIn](https://www.linkedin.com/in/truett-bloxsom/), [github](https://github.com/tsbloxsom) 

This is my first interactive dashboard using Dash! Hope you like it!

If you would like to read about how I created this I wrote a medium [article] (https://towardsdatascience.com/creating-and-automating-an-interactive-dashboard-using-python-5d9dfa170206)

This first plot is Texas COVID-19 accumulated cases by county over time

This plot is interactive, so you can double click one county to look at it individually

Source for data: [dshs.texas.gov](https://www.dshs.texas.gov/coronavirus/additionaldata/)

'''

markdown_text_geo = '''The plot below shows COVID-19 case counts per 100,000 residents for each county in the past 7 days

The major cities are plotted in grey and you must zoom in to interact with the counites in and around these cities

Population of counties is based on 2010 Texas census data, and I will be writing a medium article about this plot soon!

'''

app.layout = html.Div([
    dcc.Markdown(children=markdown_text,
        style={
            'backgroundColor': colors['background'],
            'textAlign': 'center',
            'color': colors['text']
        }),
    
    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
            
     dcc.Markdown(children=markdown_text_geo,
        style={
            'backgroundColor': colors['background'],
            'textAlign': 'center',
            'color': colors['text']
        }),

    dcc.Graph(
            id = "graph2",
            figure = fig2),

    dcc.Graph(
            id = "graph3",
            figure = fig3)
    
])


if __name__ == '__main__':
    app.run_server(debug=True)
