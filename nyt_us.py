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
# selected = input("Enter name of state: ")

# extract covid-19 data from NYtimes github
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
data = pd.read_csv(url, error_bad_lines=False)

# turn the read csv into a pandas DataFrame
df = pd.DataFrame(data)
#print (df)

# group the data for US as a whole
us = df.groupby(['date']).agg({'cases':'sum','deaths':'sum'})

# the grouped by Date column from above becomes the index to the table
# this turns the Date Index into a useable column in the dataframe
us.reset_index(inplace=True)

# Other data transformations for statistics
us['lag_cases']         = us['cases'].shift(1)
us['lag_deaths']        = us['deaths'].shift(1)
us['new_cases']         = us['cases'] - us['lag_cases']
us['new_deaths']        = us['deaths'] - us['lag_deaths']
us['yesterday_cases']   = us['new_cases'].shift(1)
us['yesterday_deaths']  = us['new_deaths'].shift(1)
us['case_growth_rate']  = (us['new_cases'] / us['yesterday_cases']) - 1
us['death_growth_rate'] = (us['new_deaths'] / us['yesterday_deaths']) - 1
us['case_mvg_avg']      = us['case_growth_rate'].rolling(7).mean()
us['death_mvg_avg']     = us['death_growth_rate'].rolling(7).mean()
us['new_case_7day_avg'] = us['new_cases'].rolling(7).mean()
us['death_7day_avg']    = us['new_deaths'].rolling(7).mean()

print ("US data set after additional transformations: \n", us)

# assign columns to variables
us_dt          = us[["date"]]
us_cs          = us[["cases"]]
us_nc          = us[["new_cases"]]
us_deaths      = us[["deaths"]]
us_nd          = us[["new_deaths"]]
us_cgr         = us[["case_growth_rate"]]
us_avg_cgr     = us[["case_mvg_avg"]]
us_dgr         = us[["death_growth_rate"]]
us_avg_dgr     = us[["death_mvg_avg"]]
us_avg_nc      = us[["new_case_7day_avg"]]
us_avg_deaths  = us[["death_7day_avg"]]

# turn the dataframe values into lists
us_date_list       = us_dt.values.tolist()
us_death_list      = us_deaths.values.tolist()
us_case_list       = us_cs.values.tolist()
us_new_case_list   = us_nc.values.tolist()
us_num_list        = range(0, len(us_case_list))



# make the variable names a little easier to use for plots
us_x    = us_num_list
us_y1   = us_case_list
us_y2   = us_death_list
us_y3   = us_new_case_list
us_y10  = us_nd
us_y4   = us_cgr
us_y5   = us_avg_cgr
us_y6   = us_dgr
us_y7   = us_avg_dgr
us_y8   = us_avg_nc 
us_y9   = us_avg_deaths

print ("Okay, let's plot US data, with data from %r to %r" % (us_date_list[0], us_date_list[-1]))

# plot New Cases Daily
plt.plot(us_x, us_y3, linestyle="dashed", label="Daily New Cases")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(us_x, us_y8, linestyle="dashed", label="7-day Avg New Cases")#, data=df, marker='', color='olive', linewidth=2)
plt.title("US")
plt.title(us_date_list[0], loc='left')
plt.title(us_date_list[-1], loc='right')
plt.legend()
plt.show()

# plot Deaths Daily
plt.plot(us_x, us_y10, linestyle="dashed", label="Daily New Deaths")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(us_x, us_y9, linestyle="dashed", label="7-day Avg Deaths")#, data=df, marker='', color='olive', linewidth=2)
plt.title("US")
plt.title(us_date_list[0], loc='left')
plt.title(us_date_list[-1], loc='right')
plt.legend()
plt.show()

# Plot Growth Rates
plt.plot(us_x, us_y5, linestyle="dashed", label="3-Day Avg Growth Rate: New Cases")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(us_x, us_y7, linestyle="dashed", label="3-Day Avg Growth Rate: New Deaths")#, data=df, marker='', color='olive', linewidth=2)
plt.title("US")
plt.title(us_date_list[0], loc='left')
plt.title(us_date_list[-1], loc='right')
plt.legend()
plt.show()
