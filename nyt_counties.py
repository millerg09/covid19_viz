# import_nytimes_dataset.py

# raw source file = https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv
# github repo = https://github.com/nytimes/covid-19-data

# import your modules

print ("Module import started\n")
from sys import argv

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange)
import datetime

print ("Module import complete!\n")

plt.close('all')

# TO DO: come back and make it so you can make a state an argument / variable
#script, state = argv

# ask user for what county they're interested in
selected_county = input("Enter name of county: ")
selected_state = input("Enter the state of the requested county: ")

# extract covid-19 data from NYtimes github
print ("Fetching NYT dataset started\n")

url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
data = pd.read_csv(url, error_bad_lines=False)

print ("Fetching NYT dataset complete!\n")

# print data
# print data.describe()

print ("Starting data transformations\n")

# turn the read csv into a pandas DataFrame
df = pd.DataFrame(data)

# filter the dataframe to selected state
selection_county = df['county'] == selected_county
#ct_df['county'] == selected_county
#ct_df['state'] == selected_state
ct = df[(df['county']==selected_county) & (df['state']==selected_state)]

#ct['double_cases'] = ct['cases']*2
ct['lag_cases']         = ct['cases'].shift(1)
ct['lag_deaths']        = ct['deaths'].shift(1)
ct['new_cases']         = ct['cases'] - ct['lag_cases']
ct['new_deaths']        = ct['deaths'] - ct['lag_deaths']
ct['yesterday_cases']   = ct['new_cases'].shift(1)
ct['yesterday_deaths']  = ct['new_deaths'].shift(1)
ct['case_growth_rate']  = (ct['new_cases'] / ct['yesterday_cases']) - 1
ct['death_growth_rate'] = (ct['new_deaths'] / ct['yesterday_deaths']) - 1
ct['case_mvg_avg']      = ct['case_growth_rate'].rolling(3).mean()
ct['death_mvg_avg']     = ct['death_growth_rate'].rolling(3).mean()
ct['new_case_7day_avg'] = ct['new_cases'].rolling(7).mean()
ct['death_7day_avg']    = ct['new_deaths'].rolling(7).mean()

# print the entire filtered dataframe
#print (ct)

# print a few columns of the dataframe
#print ct[["date", "state", "cases"]]

# assign columns to variables
dt          = ct[["date"]]
cs          = ct[["cases"]]
nc          = ct[["new_cases"]]
deaths      = ct[["deaths"]]
nd          = ct[["new_deaths"]]
cgr         = ct[["case_growth_rate"]]
avg_cgr     = ct[["case_mvg_avg"]]
dgr         = ct[["death_growth_rate"]]
avg_dgr     = ct[["death_mvg_avg"]]
avg_nc      = ct[["new_case_7day_avg"]]
avg_deaths  = ct[["death_7day_avg"]]

### debug the data types
# print (type(ct), type(dt), type(cs), type(deaths))

# turn the dataframe values into lists
date_list = dt.values.tolist()
death_list = deaths.values.tolist()
case_list = cs.values.tolist()
new_case_list = nc.values.tolist()
num_list = range(0, len(case_list))

### debug the type of the data, hopefully they're lists
# print (type(date_list), type(case_list), type(death_list), type(num_list))

### print the actual data

#print ('\n\n', date_list, '\n\n')
#print ('\n\n', case_list, '\n\n')
#print ('\n\n', death_list, '\n\n')
#print ('\n\n', num_list, '\n\n')


### print the number of objects in each list, to make sure they're equal
# print (len(case_list), len(num_list))

print ("Data transformations complete!\n")

print ("Begin plotting data\n")

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

print ("Okay, let's plot %s county." % selected_county)

# plot New Cases Daily
plt.plot(x, y3, linestyle="dashed", label="Daily New Cases")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(x, y8, linestyle="dashed", label="7-day Avg New Cases")#, data=df, marker='', color='olive', linewidth=2)
plt.title(selected_county)
plt.title(date_list[0], loc='left')
plt.title(date_list[-1], loc='right')
plt.legend()
plt.show()

# plot Deaths Daily
plt.plot(x, y10, linestyle="dashed", label="Daily New Deaths")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(x, y9, linestyle="dashed", label="7-day Avg Deaths")#, data=df, marker='', color='olive', linewidth=2)
plt.title(selected_county)
plt.title(date_list[0], loc='left')
plt.title(date_list[-1], loc='right')
plt.legend()
plt.show()

# Plot Growth Rates
plt.plot(x, y5, linestyle="dashed", label="3-Day Avg Growth Rate: New Cases")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(x, y7, linestyle="dashed", label="3-Day Avg Growth Rate: New Deaths")#, data=df, marker='', color='olive', linewidth=2)
plt.title(selected_county)
plt.title(date_list[0], loc='left')
plt.title(date_list[-1], loc='right')
plt.legend()
plt.show()
