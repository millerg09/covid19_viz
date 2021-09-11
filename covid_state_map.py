
### import your modules
from sys import argv
from datetime import date 
from datetime import timedelta 
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
from matplotlib.dates import (YEARLY, DateFormatter, rrulewrapper, RRuleLocator, drange)
import datetime

### general setup
pd.set_option('display.max_rows', 1000)
plt.close('all')

### extract covid-19 data from NYtimes github
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
data = pd.read_csv(url, error_bad_lines=False)

census_csv = pd.read_csv('/Users/gabriel.miller/Desktop/python/covid19/census/county_pop.csv', error_bad_lines=False, encoding = "utf-8")

### print data
# print data.describe()

### turn the read csv into a pandas DataFrame
df = pd.DataFrame(data)
df = df.sort_values(by=['state', 'county', 'date'], ascending=True)
#print ("\n\nprinting regular dateframe", (df))

### see unique list of counties included
#df['state_county'] = df['county'] + ' County, ' + df['state']
#state_county_list = list(df.state_county.unique())

# create a joinable column in the nyt dataset
df['join_key'] = df['county'] + ' County ' + df['state']
census_csv['join_key'] = census_csv['county'] + ' ' + census_csv['state']

df = df.join(census_csv.set_index('join_key'), on='join_key',  how = 'left', lsuffix = '_left', rsuffix = '_right')

### create new metrics from base table
df['lag_cases']         = df['cases'].shift(1)
df['lag_deaths']        = df['deaths'].shift(1)
df['new_cases']         = df['cases'] - df['lag_cases']
df['new_deaths']        = df['deaths'] - df['lag_deaths']
df['yesterday_cases']   = df['new_cases'].shift(1)
df['yesterday_deaths']  = df['new_deaths'].shift(1)
df['case_growth_rate']  = (df['new_cases'] / df['yesterday_cases']) - 1
df['death_growth_rate'] = (df['new_deaths'] / df['yesterday_deaths']) - 1
df['case_mvg_avg']      = df['case_growth_rate'].rolling(7).mean()
df['death_mvg_avg']     = df['death_growth_rate'].rolling(7).mean()
df['new_case_7day_avg'] = df['new_cases'].rolling(7).mean()
df['death_7day_avg']    = df['new_deaths'].rolling(7).mean()
df['growth_factor']     = df['new_case_7day_avg'] * df['case_mvg_avg']
df['nc_per_capita']     = df['new_cases'] / df['population']
df['nc_7day_per_capita']= df['new_case_7day_avg'] / df['population']
df['nc_7day_per_100k']  = round(df['nc_7day_per_capita'] * 100000, 0)


## week over week
df['lag_cases_7day']        = df['cases'].shift(7)
df['new_cases_this_week']   = df['new_cases'].rolling(7).sum()
df['new_cases_14day']       = df['new_cases'].rolling(14).sum()
df['new_cases_last_week']   = df['new_cases_14day'] - df['new_cases_this_week']
df['week_over_week_growth'] = df['new_cases_this_week'] - df['new_cases_last_week']
df['week_growth_rate']      = df['week_over_week_growth'] / df['new_cases_last_week']
df['weekly_growth_factor']  = df['week_growth_rate'] * df['new_cases_this_week']
df['wow_growth_per_capita'] = df['week_over_week_growth'] / df['population']

df['date'] = pd.to_datetime(df['date']) 

df = df[[
        'date', 'state_right', 'fips', 'cases', 'deaths', 
        'new_cases', 'yesterday_cases', 'new_deaths', 'case_growth_rate', 
        'death_growth_rate', 'case_mvg_avg', 'new_case_7day_avg', 
        'death_7day_avg', 'growth_factor', 'new_cases_this_week', 
        'week_over_week_growth', 'week_growth_rate', 'weekly_growth_factor', 
        'nc_per_capita', 'nc_7day_per_capita', 'wow_growth_per_capita', 'nc_7day_per_100k'
        ]]

###############################################

### filter data to latest date
max_date = df['date'].max()
print ("\nRunning report on: ", max_date, '\n')
selection =  df['date'] == max_date
df = df[selection]

### filter out null fips
df = df[df['fips'].notnull()]


### filter data to user selection
selected_state = input("Enter name of state: ")
selected_abb = input("Enter abbreviation of the state: ")
selected_abb = list(selected_abb)

selection = df['state_right'] == selected_state
df = df[selection]

#df_sample = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/minoritymajority.csv')
#df_sample_r = df_sample[df_sample['STNAME'] == selected_state]


values = df['nc_7day_per_100k'].tolist()
fips = df['fips'].tolist()

df = df[[
        'fips', 'nc_7day_per_100k'
        ]]

#print(df)

print(values)
print(fips)

colorscale_blue = [
    'rgb(193, 193, 193)',
    'rgb(239,239,239)',
    'rgb(195, 196, 222)',
    'rgb(144,148,194)',
    'rgb(101,104,168)',
    'rgb(65, 53, 132)'
]

colorscale_red = [
'rgb(255, 252, 252)',
'rgb(255, 210,  210)',
'rgb(255, 168,  168)',
'rgb(255, 126,  126)',
'rgb(255, 84,  84)',
'rgb(255, 42,  42)'
]

fig = ff.create_choropleth(
    fips=fips, 
    values=values, 
    scope=selected_abb,
    binning_endpoints=[0, 50, 100, 150, 200], 
    colorscale=colorscale_red,
    county_outline={'color': 'rgb(255,255,255)', 'width': 1.5}, 
    round_legend_values=True,
    legend_title='COVID-19 Cases per 100k Citizens by County', 
    title='%s COVID-19 by County' % selected_state
)
fig.layout.template = None
fig.show()
