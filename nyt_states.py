# import_nytimes_dataset.py

# raw source file = https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv
# github repo = https://github.com/nytimes/covid-19-data

# import your modules
from sys import argv

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange)
import datetime

plt.close('all')

# ask user for what county they're interested in
selected = input("Enter name of state: ")

# extract covid-19 data from NYtimes github
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
data = pd.read_csv(url, error_bad_lines=False)

# turn the read csv into a pandas DataFrame
df = pd.DataFrame(data)

# filter the dataframe to selected state
selection =  df['state'] == selected
fd = df[selection]

#fd['double_cases'] = fd['cases']*2
fd['lag_cases']         = fd['cases'].shift(1)
fd['lag_deaths']        = fd['deaths'].shift(1)
fd['new_cases']         = fd['cases'] - fd['lag_cases']
fd['new_deaths']        = fd['deaths'] - fd['lag_deaths']
fd['yesterday_cases']   = fd['new_cases'].shift(1)
fd['yesterday_deaths']  = fd['new_deaths'].shift(1)
fd['case_growth_rate']  = (fd['new_cases'] / fd['yesterday_cases']) - 1
fd['death_growth_rate'] = (fd['new_deaths'] / fd['yesterday_deaths']) - 1
fd['case_mvg_avg']      = fd['case_growth_rate'].rolling(7).mean()
fd['death_mvg_avg']     = fd['death_growth_rate'].rolling(7).mean()
fd['new_case_7day_avg'] = fd['new_cases'].rolling(7).mean()
fd['death_7day_avg']    = fd['new_deaths'].rolling(7).mean()

# print the entire filtered dataframe
print (fd)

# assign columns to variables
dt          = fd[["date"]]
cs          = fd[["cases"]]
nc          = fd[["new_cases"]]
deaths      = fd[["deaths"]]
nd          = fd[["new_deaths"]]
cgr         = fd[["case_growth_rate"]]
avg_cgr     = fd[["case_mvg_avg"]]
dgr         = fd[["death_growth_rate"]]
avg_dgr     = fd[["death_mvg_avg"]]
avg_nc      = fd[["new_case_7day_avg"]]
avg_deaths  = fd[["death_7day_avg"]]

# turn the dataframe values into lists
date_list = dt.values.tolist()
death_list = deaths.values.tolist()
case_list = cs.values.tolist()
new_case_list = nc.values.tolist()
num_list = range(0, len(case_list))

# make the variable names a little easier to use for plots
x = num_list
y1 = case_list
y2 = death_list
y3 = new_case_list
y10 = nd
y4 = cgr
y5 = avg_cgr
y6 = dgr
y7 = avg_dgr
y8 = avg_nc 
y9 = avg_deaths

print ("Okay, let's plot %s state, with data from %r to %r" % (selected, date_list[0], date_list[-1]))

# plot New Cases Daily
plt.plot(x, y3, linestyle="dashed", label="Daily New Cases")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(x, y8, linestyle="dashed", label="7-day Avg New Cases")#, data=df, marker='', color='olive', linewidth=2)
plt.title(selected)
plt.title(date_list[0], loc='left')
plt.title(date_list[-1], loc='right')
plt.legend()
plt.show()

# plot Deaths Daily
plt.plot(x, y10, linestyle="dashed", label="Daily New Deaths")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(x, y9, linestyle="dashed", label="7-day Avg Deaths")#, data=df, marker='', color='olive', linewidth=2)
plt.title(selected)
plt.title(date_list[0], loc='left')
plt.title(date_list[-1], loc='right')
plt.legend()
plt.show()

# Plot Growth Rates
plt.plot(x, y5, linestyle="dashed", label="3-Day Avg Growth Rate: New Cases")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(x, y7, linestyle="dashed", label="3-Day Avg Growth Rate: New Deaths")#, data=df, marker='', color='olive', linewidth=2)
plt.title(selected)
plt.title(date_list[0], loc='left')
plt.title(date_list[-1], loc='right')
plt.legend()
plt.show()
