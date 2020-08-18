# import_nytimes_dataset.py

# raw source file = https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv
# github repo = https://github.com/nytimes/covid-19-data

### import your modules
from sys import argv
from datetime import date 
from datetime import timedelta 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import (YEARLY, DateFormatter, rrulewrapper, RRuleLocator, drange)
import datetime
import plotly.express as px
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

### general setup
pd.set_option('display.max_rows', 10)
plt.close('all')

### extract covid-19 data from NYtimes github
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
data = pd.read_csv(url, error_bad_lines=False)

### print data
print (data.describe())

### turn the read csv into a pandas DataFrame
df = pd.DataFrame(data)
df = df.sort_values(by=['state', 'date'], ascending=True)
print ("\n\nprinting regular dateframe", (df))

### create new metrics from base table
df['lag_cases']         = df['cases'].shift(1)
df['lag_deaths']        = df['deaths'].shift(1)
df['new_cases']         = df['cases'] - df['lag_cases']
df['new_deaths']        = df['deaths'] - df['lag_deaths']
df['yesterday_cases']   = df['new_cases'].shift(1)
df['yesterday_deaths']  = df['new_deaths'].shift(1)
df['case_growth_rate']  = (df['new_cases'] / df['yesterday_cases']) - 1
df['death_growth_rate'] = (df['new_deaths'] / df['yesterday_deaths']) - 1
df['case_mvg_avg']      = df['case_growth_rate'].rolling(3).mean()
df['death_mvg_avg']     = df['death_growth_rate'].rolling(3).mean()
df['new_case_7day_avg'] = df['new_cases'].rolling(7).mean()
df['death_7day_avg']    = df['new_deaths'].rolling(7).mean()
df['growth_factor']     = df['new_cases'] * df['case_growth_rate']

### check the metrics
# print ("\n\nprinting transformed dataframe", (df))

### filter data to latest date
max_date = df['date'].max()
print ("\nRunning report on: ", max_date, '\n')
selection =  df['date'] == max_date
df = df[selection]

### print off your summary of results
df = df[[
    'date', 'state', 'fips', 
    'cases', 'deaths', 'new_cases', 'yesterday_cases', 
    'new_deaths', 'case_growth_rate', 'death_growth_rate', 
    'case_mvg_avg', 'new_case_7day_avg', 'death_7day_avg', 
    'growth_factor'
    ]]

df = df[['fips', 'state', 'growth_factor', 'new_case_7day_avg']]

non_zero =  df['fips'] >= 0
df = df[non_zero]
non_inf = df['growth_factor'] <= 10000000
df = df[non_inf]

df["fips"] = df["fips"].astype(float).astype(int)
# print(df.dtypes)

max_growth = df['growth_factor'].max()
max_nc = df['new_case_7day_avg'].max()

print ("The max growth for the period is: %s" % max_growth)
print ("The max avg new cases for the period is: %s" % max_nc)

# print (df)

fig = px.choropleth(
                    locations='states', 
                    locationmode="USA-states", 
                    #color=[1,2,3], 
                    color='new_case_7day_avg',
                    color_continuous_scale="Viridis",
                    mapbox_style="carto-positron",
                    zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                    opacity=0.5,
                    labels={'fips':'state_county'}
                    scope="usa")
fig.show()

"""
fig = px.choropleth_mapbox(df, geojson=counties, locations='fips', color='new_case_7day_avg',
                           color_continuous_scale="Viridis",
                           range_color=(0, max_nc),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'fips':'state_county'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
"""