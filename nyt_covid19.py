
### Utilized Datasets
# US (agg from state) source file = # States source file = https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv
# States source file = https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv
# Counties source file = https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv
# github repo = https://github.com/nytimes/covid-19-data

### import your modules
from sys import argv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange)
import datetime

plt.close('all')

### user input variables
selected_state = input("Enter name of state: ")
selected_county = input("Enter name of county: ")

### USA ###

print ("Fetching NYT `states` dataset\n")

# extract covid-19 data from NYtimes github
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
us_data = pd.read_csv(url, error_bad_lines=False)

print ("Fetching complete!\n")

print ("Beginning data transformations\n")

# turn the read csv into a pandas DataFrame
us_df = pd.DataFrame(us_data)
#print (df)

# group the data for US as a whole
us = us_df.groupby(['date']).agg({'cases':'sum','deaths':'sum'})

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

## week over week
us['lag_cases_7day']        = us['cases'].shift(7)
us['new_cases_this_week']   = us['new_cases'].rolling(7).sum()
us['new_cases_14day']       = us['new_cases'].rolling(14).sum()
us['new_cases_last_week']   = us['new_cases_14day'] - us['new_cases_this_week']
us['week_over_week_growth'] = us['new_cases_this_week'] - us['new_cases_last_week']
us['week_growth_rate']      = us['week_over_week_growth'] / us['new_cases_last_week']

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

print ("Data transformations complete!\n")

"""
print ("Okay, let's plot US data, with data from %r to %r" % (us_date_list[0], us_date_list[-1]))

# plot US New Cases Daily
plt.plot(us_x, us_y3, linestyle="dashed", label="Daily New Cases")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(us_x, us_y8, linestyle="dashed", label="7-day Avg New Cases")#, data=df, marker='', color='olive', linewidth=2)
plt.title("United States")
plt.title(us_date_list[0], loc='left')
plt.title(us_date_list[-1], loc='right')
plt.legend()
plt.show()

# plot US Deaths Daily
plt.plot(us_x, us_y10, linestyle="dashed", label="Daily New Deaths")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(us_x, us_y9, linestyle="dashed", label="7-day Avg Deaths")#, data=df, marker='', color='olive', linewidth=2)
plt.title("United States")
plt.title(us_date_list[0], loc='left')
plt.title(us_date_list[-1], loc='right')
plt.legend()
plt.show()

# Plot US Growth Rates
plt.plot(us_x, us_y5, linestyle="dashed", label="3-Day Avg Growth Rate: New Cases")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(us_x, us_y7, linestyle="dashed", label="3-Day Avg Growth Rate: New Deaths")#, data=df, marker='', color='olive', linewidth=2)
plt.title("United States")
plt.title(us_date_list[0], loc='left')
plt.title(us_date_list[-1], loc='right')
plt.legend()
plt.show()
"""

### STATES ###

print ("Fetching NYT `counties` dataset\n")

# ask user for what county they're interested in
#selected_state = input("Enter name of state: ")

# extract covid-19 data from NYtimes github
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
st_data = pd.read_csv(url, error_bad_lines=False)

print ("Fetching complete!\n")

print ("Beginning data transformations\n")

# turn the read csv into a pandas DataFrame
st_df = pd.DataFrame(st_data)

# filter the dataframe to selected state
selection_state =  st_df['state'] == selected_state
st = st_df[selection_state]

#st['double_cases'] = st['cases']*2
st['lag_cases']         = st['cases'].shift(1)
st['lag_deaths']        = st['deaths'].shift(1)
st['new_cases']         = st['cases'] - st['lag_cases']
st['new_deaths']        = st['deaths'] - st['lag_deaths']
st['yesterday_cases']   = st['new_cases'].shift(1)
st['yesterday_deaths']  = st['new_deaths'].shift(1)
st['case_growth_rate']  = (st['new_cases'] / st['yesterday_cases']) - 1
st['death_growth_rate'] = (st['new_deaths'] / st['yesterday_deaths']) - 1
st['case_mvg_avg']      = st['case_growth_rate'].rolling(7).mean()
st['death_mvg_avg']     = st['death_growth_rate'].rolling(7).mean()
st['new_case_7day_avg'] = st['new_cases'].rolling(7).mean()
st['death_7day_avg']    = st['new_deaths'].rolling(7).mean()

# print the entire filtered dataframe
#print (st)

# assign columns to variables
st_dt          = st[["date"]]
st_cs          = st[["cases"]]
st_nc          = st[["new_cases"]]
st_deaths      = st[["deaths"]]
st_nd          = st[["new_deaths"]]
st_cgr         = st[["case_growth_rate"]]
st_avg_cgr     = st[["case_mvg_avg"]]
st_dgr         = st[["death_growth_rate"]]
st_avg_dgr     = st[["death_mvg_avg"]]
st_avg_nc      = st[["new_case_7day_avg"]]
st_avg_deaths  = st[["death_7day_avg"]]

# turn the dataframe values into lists
st_date_list = st_dt.values.tolist()
st_death_list = st_deaths.values.tolist()
st_case_list = st_cs.values.tolist()
st_new_case_list = st_nc.values.tolist()
st_num_list = range(0, len(st_case_list))

# make the variable names a little easier to use for plots
st_x = st_num_list
st_y1 = st_case_list
st_y2 = st_death_list
st_y3 = st_new_case_list
st_y10 = st_nd
st_y4 = st_cgr
st_y5 = st_avg_cgr
st_y6 = st_dgr
st_y7 = st_avg_dgr
st_y8 = st_avg_nc 
st_y9 = st_avg_deaths
"""
print ("Okay, let's plot %s state, with data from %r to %r" % (selected_state, st_date_list[0], st_date_list[-1]))

# plot State New Cases Daily
plt.plot(st_x, st_y3, linestyle="dashed", label="Daily New Cases")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(st_x, st_y8, linestyle="dashed", label="7-day Avg New Cases")#, data=df, marker='', color='olive', linewidth=2)
plt.title(selected_state)
plt.title(st_date_list[0], loc='left')
plt.title(st_date_list[-1], loc='right')
plt.legend()
plt.show()

# plot State Deaths Daily
plt.plot(st_x, st_y10, linestyle="dashed", label="Daily New Deaths")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(st_x, st_y9, linestyle="dashed", label="7-day Avg Deaths")#, data=df, marker='', color='olive', linewidth=2)
plt.title(selected_state)
plt.title(st_date_list[0], loc='left')
plt.title(st_date_list[-1], loc='right')
plt.legend()
plt.show()

# Plot State Growth Rates
plt.plot(st_x, st_y5, linestyle="dashed", label="3-Day Avg Growth Rate: New Cases")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(st_x, st_y7, linestyle="dashed", label="3-Day Avg Growth Rate: New Deaths")#, data=df, marker='', color='olive', linewidth=2)
plt.title(selected_state)
plt.title(st_date_list[0], loc='left')
plt.title(st_date_list[-1], loc='right')
plt.legend()
plt.show()
"""

print ("Data transformations complete\n")

### COUNTY

print ("Fetching NYT `counties` dataset... again\n")

# extract covid-19 data from NYtimes github
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
ct_data = pd.read_csv(url, error_bad_lines=False)

print ("Fetch complete!\n")

# print data
# print data.describe()

print ("Beginning data transformations\n")

# turn the read csv into a pandas DataFrame
ct_df = pd.DataFrame(ct_data)

# filter the dataframe to selected county
selection_county = ct_df['county'] == selected_county
ct_df['county'] == selected_county
ct_df['state'] == selected_state
ct = ct_df[(ct_df['county']==selected_county) & (ct_df['state']==selected_state)]

#print (ct)

#ct['double_cases'] = ct['cases']*2
ct['lag_cases']         = ct['cases'].shift(1)
ct['lag_deaths']        = ct['deaths'].shift(1)
ct['new_cases']         = ct['cases'] - ct['lag_cases']
ct['new_deaths']        = ct['deaths'] - ct['lag_deaths']
ct['yesterday_cases']   = ct['new_cases'].shift(1)
ct['yesterday_deaths']  = ct['new_deaths'].shift(1)
ct['case_growth_rate']  = (ct['new_cases'] / ct['yesterday_cases']) - 1
ct['death_growth_rate'] = (ct['new_deaths'] / ct['yesterday_deaths']) - 1
ct['case_mvg_avg']      = ct['case_growth_rate'].rolling(7).mean()
ct['death_mvg_avg']     = ct['death_growth_rate'].rolling(7).mean()
ct['new_case_7day_avg'] = ct['new_cases'].rolling(7).mean()
ct['death_7day_avg']    = ct['new_deaths'].rolling(7).mean()

# print the entire filtered dataframe
#print (ct)

# print a few columns of the dataframe
#print ct[["date", "state", "cases"]]

# assign columns to variables
ct_dt          = ct[["date"]]
ct_cs          = ct[["cases"]]
ct_nc          = ct[["new_cases"]]
ct_deaths      = ct[["deaths"]]
ct_nd          = ct[["new_deaths"]]
ct_cgr         = ct[["case_growth_rate"]]
ct_avg_cgr     = ct[["case_mvg_avg"]]
ct_dgr         = ct[["death_growth_rate"]]
ct_avg_dgr     = ct[["death_mvg_avg"]]
ct_avg_nc      = ct[["new_case_7day_avg"]]
ct_avg_deaths  = ct[["death_7day_avg"]]

### debug the data types
# print (type(ct), type(dt), type(cs), type(deaths))

# turn the dataframe values into lists
ct_date_list       = ct_dt.values.tolist()
ct_death_list      = ct_deaths.values.tolist()
ct_case_list       = ct_cs.values.tolist()
ct_new_case_list   = ct_nc.values.tolist()
ct_num_list        = range(0, len(ct_case_list))

### debug the type of the data, hopefully they're lists
# print (type(date_list), type(case_list), type(death_list), type(num_list))

### print the actual data

#print ('\n\n', date_list, '\n\n')
#print ('\n\n', case_list, '\n\n')
#print ('\n\n', death_list, '\n\n')
#print ('\n\n', num_list, '\n\n')


### print the number of objects in each list, to make sure they're equal
# print (len(case_list), len(num_list))

# make the variable names a little easier to use for plots
ct_x = ct_num_list
ct_y1 = ct_case_list
ct_y2 = ct_death_list
ct_y3 = ct_new_case_list
ct_y10 = ct_nd
ct_y4 = ct_cgr
ct_y5 = ct_avg_cgr
ct_y6 = ct_dgr
ct_y7 = ct_avg_dgr
ct_y8 = ct_avg_nc 
ct_y9 = ct_avg_deaths

print ("Data transformations complete\n")

"""
print ("Okay, let's plot %s county." % selected_county)

# plot New Cases Daily
plt.plot(ct_x, ct_y3, linestyle="dashed", label="Daily New Cases")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(ct_x, ct_y8, linestyle="dashed", label="7-day Avg New Cases")#, data=df, marker='', color='olive', linewidth=2)
plt.title(selected_county)
plt.title(ct_date_list[0], loc='left')
plt.title(ct_date_list[-1], loc='right')
plt.legend()
plt.show()

# plot Deaths Daily
plt.plot(ct_x, ct_y10, linestyle="dashed", label="Daily New Deaths")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(ct_x, ct_y9, linestyle="dashed", label="7-day Avg Deaths")#, data=df, marker='', color='olive', linewidth=2)
plt.title(selected_county)
plt.title(ct_date_list[0], loc='left')
plt.title(ct_date_list[-1], loc='right')
plt.legend()
plt.show()

# Plot Growth Rates
plt.plot(ct_x, ct_y5, linestyle="dashed", label="3-Day Avg Growth Rate: New Cases")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(ct_x, ct_y7, linestyle="dashed", label="3-Day Avg Growth Rate: New Deaths")#, data=df, marker='', color='olive', linewidth=2)
plt.title(selected_county)
plt.title(ct_date_list[0], loc='left')
plt.title(ct_date_list[-1], loc='right')
plt.legend()
plt.show()
"""

### Try plotting them all at the same time
fig, axs = plt.subplots(3, 2)
axs[1, 0].plot(st_x, st_y8)
axs[1, 0].set_title('%s State New Cases' % selected_state)
axs[1, 1].plot(st_x, st_y9, 'tab:orange')
axs[1, 1].set_title('%s State New Deaths' % selected_state)
axs[2, 0].plot(ct_x, ct_y8, 'tab:green')
axs[2, 0].set_title('%s New Cases' % selected_county)
axs[2, 1].plot(ct_x, ct_y9, 'tab:red')
axs[2, 1].set_title('%s County New Deaths' % selected_county)
axs[0, 0].plot(us_x, us_y8, 'tab:blue')
axs[0, 0].set_title('US New Cases')
axs[0, 1].plot(us_x, us_y9)
axs[0, 1].set_title('US New Deaths')

for ax in axs.flat:
    ax.set(xlabel='Days', ylabel='Amount')

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()

plt.show()

### Try plotting them all at the same time
fig, axs = plt.subplots(3, 2)
axs[1, 0].plot(st_x, st_y5)
axs[1, 0].set_title('%s State Case Growth Rate' % selected_state)
axs[1, 1].plot(st_x, st_y7, 'tab:orange')
axs[1, 1].set_title('%s State Death Growth Rate' % selected_state)
axs[2, 0].plot(ct_x, ct_y5, 'tab:green')
axs[2, 0].set_title('%s Case Growth Rate' % selected_county)
axs[2, 1].plot(ct_x, ct_y7, 'tab:red')
axs[2, 1].set_title('%s County Death Growth Rate' % selected_county)
axs[0, 0].plot(us_x, us_y5, 'tab:blue')
axs[0, 0].set_title('US Case Growth Rate')
axs[0, 1].plot(us_x, us_y7)
axs[0, 1].set_title('US Death Growth Rate')

for ax in axs.flat:
    ax.set(xlabel='Days', ylabel='Amount')

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()

plt.show()
