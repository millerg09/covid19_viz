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
import plotly.figure_factory as ff


### general setup
pd.set_option('display.max_rows', 10)
plt.close('all')

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

# thank you to @kinghelix and @trevormarburger for this idea
abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))

### extract covid-19 data from NYtimes github
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
data = pd.read_csv(url, error_bad_lines=False)

### print data
print (data.describe())

### turn the read csv into a pandas DataFrame
df = pd.DataFrame(data)
df = df.sort_values(by=['state', 'date'], ascending=True)
print ("\n\nprinting regular dateframe", (df))

df_abbrev = pd.DataFrame(list(us_state_abbrev.items()), index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                                                 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                                                                 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                                                                 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
                                                                 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
                                                                 51, 52, 53, 54, 55, 56])

df_abbrev.columns = ['state', 'abbrev']

print (df_abbrev)

df = df.set_index('state').join(df_abbrev.set_index('state'))

print (df)

df = df.reset_index()

print ("Time to reset index", df)



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
df['growth_factor']     = df['new_case_7day_avg'] * df['case_mvg_avg']

### check the metrics
# print ("\n\nprinting transformed dataframe", (df))

### filter data to latest date
max_date = df['date'].max()
print ("\nRunning report on: ", max_date, '\n')
selection =  df['date'] == max_date
df = df[selection]

### print off your summary of results
df = df[[
    'date', 'abbrev', 'fips', 'state',
    'cases', 'deaths', 'new_cases', 'yesterday_cases', 
    'new_deaths', 'case_growth_rate', 'death_growth_rate', 
    'case_mvg_avg', 'new_case_7day_avg', 'death_7day_avg', 
    'growth_factor'
    ]]

non_zero =  df['fips'] >= 0
df = df[non_zero]
non_inf = df['growth_factor'] <= 10000000
df = df[non_inf]

### Massage fips for style and compatibility
df["fips"] = df["fips"].astype(float).astype(int)
df["fips"] = df["fips"].astype(int).astype(str)
df['fips_fill'] = df['fips'].str.zfill(5)# print(df.dtypes)

### Fill in NULL holes
df = df.fillna(0)

### Calculate metrics for plot
max_growth_factor = df['growth_factor'].max()
avg_growth_factor = df['growth_factor'].mean()
max_nc = df['new_case_7day_avg'].max()
avg_nc = df['new_case_7day_avg'].mean()
max_cases = df['cases'].max()
avg_cases = df['cases'].mean()

print ("The max growth for the period is: %s" % max_growth_factor)
print ("The max avg new cases for the period is: %s" % max_nc)

fig = px.choropleth(
                    locations=df['abbrev'], 
                    locationmode="USA-states", 
                    color=df['new_case_7day_avg'],
                    color_continuous_scale="Viridis",
                    range_color=(0, avg_nc*2),
                    labels={'abbrev':'Abbrev', "cases":"Total Cases"},
                    #hover_name="state",
                    title = 'USA by COVID19 New Case 7-day Avg',
                    scope="usa")
fig.show()

fig = px.choropleth(
                    locations=df['abbrev'], 
                    locationmode="USA-states", 
                    color=df['cases'],
                    color_continuous_scale="Viridis",
                    range_color=(0, avg_cases*2),
                    labels={'abbrev':'Abbrev', "cases":"Total Cases"},
                    #hover_name="state",
                    title = 'USA by COVID19 Total Cases',
                    scope="usa")
fig.show()

fig = px.choropleth(
                    locations=df['abbrev'], 
                    locationmode="USA-states", 
                    color=df['growth_factor'],
                    color_continuous_scale="Viridis",
                    range_color=(0, avg_growth_factor*4),
                    labels={'abbrev':'Abbrev', "cases":"Total Cases"},
                    #hover_name="state",
                    title = 'USA by COVID19 Growth Factor',
                    scope="usa")
fig.show()