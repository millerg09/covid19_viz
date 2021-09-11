
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
import plotly.express as px

### Find local file and setup variables
path = '/Users/gabriel.miller/Desktop/python/covid19/census/'
state_file = 'state_pop.csv'
county_file = 'county_pop.csv'

state_filepath = (path + state_file)
county_filepath = (path + county_file)

### turn the local csv's into dataframes
state_df = pd.read_csv(state_filepath, error_bad_lines=False)
county_df = pd.read_csv(county_filepath, error_bad_lines=False, encoding='latin-1')

###TO DO, find a better way to do this
### create a dictionary of state abbreviations
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

### JOIN the datasets togethers
df_abbrev = pd.DataFrame(list(us_state_abbrev.items()), index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                                                 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                                                                 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                                                                 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
                                                                 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
                                                                 51, 52, 53, 54, 55, 56])

df_abbrev.columns = ['state', 'abbrev']

print (df_abbrev)

state_df = state_df.set_index('state').join(df_abbrev.set_index('state'))

print (state_df)

state_df = state_df.reset_index()


us_filter = state_df['state'] != 'United States'
state_df = state_df[us_filter]

#print (state_df)



state_min = state_df['population'].min()
state_max = state_df['population'].max()

### Plot the populations

fig = px.choropleth(
                    locations=state_df['abbrev'], 
                    locationmode="USA-states", 
                    color=state_df['population'],
                    color_continuous_scale="Viridis",
                    range_color=(state_min, state_max),
                    title = 'Population By State, Census 2019 Projection',
                    scope="usa")
fig.show()
