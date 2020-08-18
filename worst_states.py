# import_nytimes_dataset.py

# raw source file = https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv
# github repo = https://github.com/nytimes/covid-19-data

### import your modules
from sys import argv
from datetime import date 
from datetime import timedelta 
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import (YEARLY, DateFormatter, rrulewrapper, RRuleLocator, drange)
import datetime

### general setup
pd.set_option('display.max_rows', 1000)
plt.close('all')

### extract covid-19 data from NYtimes github
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
data = pd.read_csv(url, error_bad_lines=False)

### print data
# print data.describe()

### turn the read csv into a pandas DataFrame
df = pd.DataFrame(data)
df = df.sort_values(by=['state', 'date'], ascending=True)
#print ("\n\nprinting regular dateframe", (df))

### see unique list of states included
states = list(df.state.unique())
#states = df[['state']]
# print (type(states))
print ("\nHere are all the states: \n\n", states)

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

## week over week
df['lag_cases_7day']        = df['cases'].shift(7)
df['new_cases_this_week']   = df['new_cases'].rolling(7).sum()
df['new_cases_14day']       = df['new_cases'].rolling(14).sum()
df['new_cases_last_week']   = df['new_cases_14day'] - df['new_cases_this_week']
df['week_over_week_growth'] = df['new_cases_this_week'] - df['new_cases_last_week']
df['week_growth_rate']      = df['week_over_week_growth'] / df['new_cases_last_week']
df['weekly_growth_factor']  = df['week_growth_rate'] * df['new_cases_this_week']

### check the metrics
# print ("\n\nprinting transformed dataframe", (df))

df['date'] = pd.to_datetime(df['date']) 

### filter data to latest date
max_date = df['date'].max()
print ("\nRunning report on: ", max_date, '\n')
selection =  df['date'] == max_date
df = df[selection]

### print off your summary of results
df = df[[
        'date', 'state', 'cases', 'deaths', 
        'new_cases', 'yesterday_cases', 'new_deaths', 'case_growth_rate', 
        'death_growth_rate', 'case_mvg_avg', 'new_case_7day_avg', 
        'death_7day_avg', 'growth_factor', 'new_cases_this_week', 
        'week_over_week_growth', 'week_growth_rate', 'weekly_growth_factor'
        ]]

### Worst States Section
section = "--WORST STATES--"
print ('-'*len(section))
print (section)
print ('-'*len(section))

print ("\n\n sort by worst new cases\n\n", df[['date', 'state', 'new_cases']].sort_values(by=['new_cases'], ascending=False).head(10))
print ("\n\n sort by worst 7day avg\n\n", df[['date', 'state', 'new_case_7day_avg']].sort_values(by=['new_case_7day_avg'], ascending=False).head(10))
print ("\n\n sort by worst growth factor (new cases * growth rate of cases)\n\n", df[['date', 'state', 'growth_factor']].sort_values(by=['growth_factor'], ascending=False).head(10))

df2 = df[df['week_growth_rate'].between(-100, 100)]

print ("\n\n sort by worst weekly growth\n\n", df2[['date', 'state','week_over_week_growth']].sort_values(by=['week_over_week_growth'], ascending=False).head(10))
print ("\n\n sort by worst weekly growth rate\n\n", df2[['date', 'state', 'week_growth_rate']].sort_values(by=['week_growth_rate'], ascending=False).head(10))
print ("\n\n sort by worst weekly growth factor\n\n", df2[['date', 'state', 'weekly_growth_factor']].sort_values(by=['weekly_growth_factor'], ascending=False).head(10))
print ("\n\n")

### Best States Section
section = "--BEST STATES--"
print ('-'*len(section))
print (section)
print ('-'*len(section))

print ("\n\n sort by lowest new cases\n\n", df[['date', 'state', 'new_cases']].sort_values(by=['new_cases'], ascending=True).head(10))
print ("\n\n sort by lowest 7day avg\n\n", df[['date', 'state', 'new_case_7day_avg']].sort_values(by=['new_case_7day_avg'], ascending=True).head(10))
# print ("\n\n sort by worst growth rate\n\n", df[['date', 'state', 'case_growth_rate']].sort_values(by=['case_growth_rate'], ascending=True).head(10))
# print ("\n\n sort by worst avg new cases\n\n", df[['date', 'state', 'case_mvg_avg']].sort_values(by=['case_mvg_avg'], ascending=True).head(10))
print ("\n\n sort by lowest growth factor (new cases * growth rate of cases)\n\n", df[['date', 'state', 'growth_factor']].sort_values(by=['growth_factor'], ascending=True).head(10))
print ("\n")

### Multi filter
section = "--STATES WITH HIGH VOLUME GROWING CASES--"
print ('-'*len(section))
print (section)
print ('-'*len(section))

df2 = df
selection =  df2['case_mvg_avg'] > 0
df2 = df2[selection]
selection2 =  df2['case_growth_rate'] > 0
df2 = df2[selection2]
# print (df2[selection2])

print ("\n\n sort by worst growth factor\n\n", df2[['date', 'state', 'cases', 'deaths', 'new_cases', 'case_growth_rate', 'death_growth_rate', 'case_mvg_avg', 'new_case_7day_avg', 'death_7day_avg', 'growth_factor']].sort_values(by=['growth_factor'], ascending=False).head(10))

df3 = df
selection = df3['week_growth_rate'] >= .5
df3 = df3[selection]

print ("\n\n there are ", len(df3), " states with exponential growth")

selection = df3['new_cases'] >= 300
df3 = df3[selection]

print ("\n\n there are ", len(df3), " states with exponential growth and more than 500 new cases today")

print ("\n\n potentialy expontial growth: \n\n", df3[['date', 'state', 'cases', 'deaths', 'new_cases', 'case_growth_rate', 'new_case_7day_avg', 'growth_factor', 'new_cases_this_week', 'week_growth_rate']].sort_values(by=['new_cases_this_week'], ascending=False).head(50))