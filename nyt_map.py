# import_nytimes_dataset.py

# raw source file = https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv
# github repo = https://github.com/nytimes/covid-19-data

print ("Starting script...")
print ("Fetching required modules")

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
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

### general setup
pd.set_option('display.max_rows', 10000)
plt.close('all')

print ("Module load complete!")
print ("Fetching NYTimes Data...")

### extract covid-19 data from NYtimes github
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
data = pd.read_csv(url, error_bad_lines=False)

print ("Fetch NYTimes Data complete!")
print ("Transforming the data...")

### print data
# print data.describe()

### turn the read csv into a pandas DataFrame
df = pd.DataFrame(data)
df = df.sort_values(by=['fips', 'date'], ascending=True)
print ("\n\nprinting regular dateframe", (df))

### Heal missing Fips
# 36061 = New York City

df['fips'] = np.where(df['county']=='New York City', 36061, df['fips'])

### see unique list of counties included
df['state_county'] = df['county'] + ' County, ' + df['state']
#state_county_list = list(df.state_county.unique())
#df = pd.DataFrame(state_county_list)

#print ("\nHere are all the states: \n\n", state_county_list)

df = df.sort_values(by=['fips', 'date'], ascending=True)

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

print ("Data transformation complete!")

### check the metrics
#print ("\n\nprinting transformed dataframe", (df))
#selection = df['county'] == "New York City"

#debug = df[selection]

#print (debug[['date', 'state_county', 'fips', 'cases', 'lag_cases', 'new_cases', 'yesterday_cases', 'case_growth_rate', 'case_mvg_avg', 'new_case_7day_avg', 'growth_factor']])



### filter data to latest date
max_date = df['date'].max()
#max_date = "2020-05-18"
print ("\nRunning report on: ", max_date, '\n')
selection =  df['date'] == max_date
df = df[selection]

### print off your summary of results
#df = df[['date', 'state', 'state_county', 'fips', 'county', 'cases', 'deaths', 'new_cases', 'yesterday_cases', 'new_deaths', 'case_growth_rate', 'death_growth_rate', 'case_mvg_avg', 'new_case_7day_avg', 'death_7day_avg', 'growth_factor']]
#df = df[['date', 'state', 'state_county', 'fips', 'county', 'cases', 'deaths', 'case_mvg_avg', 'new_case_7day_avg', 'growth_factor']]

non_zero    = df['fips'] >= 0
df          = df[non_zero]
#non_inf     = df['growth_factor'] <= 10000000
#df          = df[non_inf]

### unique fips checker
#df = df.groupby('date')['fips'].nunique()
#print (df)

### Massage the fips to correct style
df["fips"] = df["fips"].astype(float).astype(int)
df["fips"] = df["fips"].astype(int).astype(str)
df['fips_fill'] = df['fips'].str.zfill(5)

### Fill in NULL holes
df = df.fillna(0)

### Calculate metrics for plot
max_growth_factor = df['growth_factor'].max()
avg_growth_factor = df['growth_factor'].mean()
max_nc = df['new_case_7day_avg'].max()
avg_nc = df['new_case_7day_avg'].mean()
max_cases = df['cases'].max()
avg_cases = df['cases'].mean()
max_weekly_growth = df['week_over_week_growth'].max()
avg_weekly_growth = df['week_over_week_growth'].mean()

print ("The max growth for the period is: %s" % max_growth_factor)
print ("The avg new cases for the period is: %s" % avg_nc)
print ("The max number of cases for the period is: %s" % max_cases)
print ("The avg weekly growth for the period is: %s" % avg_weekly_growth)

print ("Plotting the data...")

fig = px.choropleth(        
                            df,     
                            geojson=counties, 
                            locations='fips_fill', 
                            color='new_case_7day_avg',
                            color_continuous_scale="Viridis",
                            range_color=(0, max_nc*.20),
                            scope="usa",
                            labels={'fips_fill':'FIPS CODE', "state":"State"},
                            hover_name="state_county",
                            hover_data=["growth_factor", "new_case_7day_avg", "new_cases", "cases"],
                            title = 'USA by COVID19 New Case 7-day Avg'
                          )
fig.update_layout(margin={"r":100,"t":100,"l":100,"b":100})
fig.show()

fig = px.choropleth(        
                            df,     
                            geojson=counties, 
                            locations='fips_fill', 
                            color='cases',
                            color_continuous_scale="Viridis",
                            range_color=(0, avg_cases),
                            scope="usa",
                            labels={'fips_fill':'FIPS CODE', "state":"State"},
                            hover_name="state_county",
                            hover_data=["growth_factor", "new_case_7day_avg", "new_cases", "cases"],
                            title = 'USA by COVID19 Total Cases'
                          )
fig.update_layout(margin={"r":100,"t":100,"l":100,"b":100})
fig.show()

fig = px.choropleth(        
                            df,     
                            geojson=counties, 
                            locations='fips_fill', 
                            color='growth_factor',
                            color_continuous_scale="Viridis",
                            range_color=(0, 100),
                            scope="usa",
                            labels={'fips_fill':'FIPS CODE', "state":"State"},
                            hover_name="state_county",
                            hover_data=["growth_factor", "new_case_7day_avg", "new_cases", "cases"],
                            title = 'USA by COVID19 Growth Factor'
                          )
fig.update_layout(margin={"r":100,"t":100,"l":100,"b":100})
fig.show()

fig = px.choropleth(        
                            df,     
                            geojson=counties, 
                            locations='fips_fill', 
                            color='week_over_week_growth',
                            color_continuous_scale="Viridis",
                            range_color=(0, 1000),
                            scope="usa",
                            labels={'fips_fill':'FIPS CODE', "state":"State"},
                            hover_name="state_county",
                            hover_data=["growth_factor", "new_case_7day_avg", "new_cases", "cases"],
                            title = 'USA by COVID19 Weekly Growth'
                          )
fig.update_layout(margin={"r":100,"t":100,"l":100,"b":100})
fig.show()

