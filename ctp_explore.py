#ctp_explore.py

# import Covid Tracking Project datasets

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

### covid tracking project urls
ctp_us_url      = 'https://covidtracking.com/api/v1/us/daily.csv'
ctp_state_url   = 'https://covidtracking.com/api/v1/states/daily.csv'

### pull and populate data
us_csv = pd.read_csv(ctp_us_url, error_bad_lines=False)
state_csv = pd.read_csv(ctp_state_url, error_bad_lines=False)

### State Prompt
selected_state = input("Enter abbreviation of state (eg. NY): ")

### US
us_df = pd.DataFrame(us_csv)
us_df = us_df[[
            "date",
            "positive",
            "negative",
            "pending",
            "hospitalizedCurrently",
            "hospitalizedCumulative",
            "inIcuCurrently",
            "inIcuCumulative",
            "recovered",
            ]]

# Transform new metrics
us_df['total_tests']    = us_df['positive'] + us_df['negative']
us_df['positive_rate']  = us_df['positive'] / us_df['total_tests']
us_df['icu_rate']       = us_df['inIcuCurrently'] / us_df['hospitalizedCurrently']
us_df['recovery_rate']  = us_df['recovered'] / us_df['positive']

# assign columns to variables
us_dt          = us_df[["date"]]
us_pos         = us_df[["positive"]]
us_neg         = us_df[["negative"]]
us_pen         = us_df[["pending"]]
us_total_test  = us_df[["total_tests"]]
us_pos_rate    = us_df[['positive_rate']]
us_icu_rate    = us_df['icu_rate']
us_rec_rate    = us_df['recovery_rate']
us_hos_curr    = us_df[["hospitalizedCurrently"]]
us_hos_cume    = us_df[["hospitalizedCumulative"]]
us_icr_curr    = us_df[["inIcuCurrently"]]
us_icr_cume    = us_df[["inIcuCumulative"]]
us_recovered   = us_df[["recovered"]]

print (us_df)

# turn the dataframe values into lists
us_date_list       = us_dt.values.tolist()
us_pos_list        = us_pos.values.tolist()
us_neg_list        = us_neg.values.tolist()
us_pen_list        = us_pen.values.tolist()
us_hos_curr_list   = us_hos_curr.values.tolist()
us_hos_cume_list   = us_hos_cume.values.tolist()

# plot values
plt.plot(us_date_list, us_hos_curr_list, label="Current Hospitalizations")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(us_date_list, us_hos_cume_list, linestyle="dashed", label="Cumulative Hospitalizations")#, data=df, marker='', color='olive', linewidth=2)
plt.title("US COVID19 Hospitalizations")
plt.legend()
plt.title(us_date_list[0], loc='left')
plt.title(us_date_list[-1], loc='right')
plt.show()

plt.plot(us_date_list, us_pos_list, label="Positive Tests")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(us_date_list, us_neg_list, label="Negative Tests")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(us_date_list, us_pen_list, label="Pending Tests")#, data=df, marker='', color='olive', linewidth=2)
plt.title("US COVID19 Test Results")
plt.legend()
plt.title(us_date_list[0], loc='left')
plt.title(us_date_list[-1], loc='right')
plt.show()

plt.plot(us_date_list, us_pos_rate, label="US Positive Test Rate")
plt.plot(us_date_list, us_icu_rate, label="US ICU Rate")
plt.plot(us_date_list, us_rec_rate, label="US Recovery Rate")
plt.title("US COVID19 Rates")
plt.legend()
plt.show()

### STATES

state_df = pd.DataFrame(state_csv)

selection_state =  state_df['state'] == selected_state
state_df = state_df[selection_state]

state_df = state_df[[
                    "date",
                    "state",
                    "fips",
                    "positive",
                    "negative",
                    "pending",
                    "hospitalizedCurrently",
                    "hospitalizedCumulative",
                    "inIcuCurrently",
                    "inIcuCumulative",
                    "recovered",
                    ]]

# Transform new metrics
state_df['total_tests']    = state_df['positive'] + state_df['negative']
state_df['positive_rate']  = state_df['positive'] / state_df['total_tests']
state_df['icu_rate']       = state_df['inIcuCurrently'] / state_df['hospitalizedCurrently']
state_df['recovery_rate']  = state_df['recovered'] / state_df['positive']

print (state_df)

# assign columns to variables
state_dt          = state_df[["date"]]
state_pos         = state_df[["positive"]]
state_neg         = state_df[["negative"]]
state_pen         = state_df[["pending"]]
state_total_test  = state_df[["total_tests"]]
state_pos_rate    = state_df[['positive_rate']]
state_icu_rate    = state_df['icu_rate']
state_rec_rate    = state_df['recovery_rate']
state_hos_curr    = state_df[["hospitalizedCurrently"]]
state_hos_cume    = state_df[["hospitalizedCumulative"]]
state_icr_curr    = state_df[["inIcuCurrently"]]
state_icr_cume    = state_df[["inIcuCumulative"]]
state_recovered   = state_df[["recovered"]]

# turn the dataframe values into lists
state_date_list       = state_dt.values.tolist()
state_pos_list        = state_pos.values.tolist()
state_neg_list        = state_neg.values.tolist()
state_pen_list        = state_pen.values.tolist()
state_hos_curr_list   = state_hos_curr.values.tolist()
state_hos_cume_list   = state_hos_cume.values.tolist()

# plot values
plt.plot(state_date_list, state_hos_curr_list, label="Current Hospitalizations")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(state_date_list, state_hos_cume_list, linestyle="dashed", label="Cumulative Hospitalizations")#, data=df, marker='', color='olive', linewidth=2)
plt.title("%s State COVID19 Hospitalizations" % selected_state)
plt.legend()
plt.title(state_date_list[0], loc='left')
plt.title(state_date_list[-1], loc='right')
plt.show()

plt.plot(state_date_list, state_pos_list, label="Positive Tests")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(state_date_list, state_neg_list, label="Negative Tests")#, data=df, marker='', color='olive', linewidth=2)
plt.plot(state_date_list, state_pen_list, label="Pending Tests")#, data=df, marker='', color='olive', linewidth=2)
plt.title("%s State COVID19 Test Results" % selected_state)
plt.legend()
plt.title(state_date_list[0], loc='left')
plt.title(state_date_list[-1], loc='right')
plt.show()

plt.plot(state_date_list, state_pos_rate, label="Positive Test Rate")
plt.plot(state_date_list, state_icu_rate, label="ICU Rate")
plt.plot(state_date_list, state_rec_rate, label="Recovery Rate")
plt.title("%s State COVID19 Rates" % selected_state)
plt.legend()
plt.show()

### Hospitalizations Metaplot
fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(us_date_list, us_hos_curr_list)
axs[0, 0].set_title("US COVID19 Current Hospitalizations")
axs[0, 1].plot(us_date_list, us_hos_cume_list)
axs[0, 1].set_title("US COVID19 Cumulative Hospitalizations")
axs[1, 0].plot(state_date_list, state_hos_curr_list)
axs[1, 0].set_title("%s State COVID19 Current Hospitalizations" % selected_state)
axs[1, 1].plot(state_date_list, state_hos_cume_list)
axs[1, 1].set_title("%s State COVID19 Cumulative Hospitalizations" % selected_state)

for ax in axs.flat:
    ax.set(xlabel='Days', ylabel='Amount')

# Hide x labels and tick labels for top plots and y ticks for right plots
for ax in axs.flat:
    ax.label_outer()

plt.show()    

### Testing Metaplot

fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(us_date_list, us_pos_list, label="Positive Tests")
axs[0, 0].plot(us_date_list, us_neg_list, label="Negative Tests")
axs[0, 0].set_title("US COVID19 Test Rates")
axs[0, 1].plot(us_date_list, us_pos_rate)
axs[0, 1].set_title("US COVID19 Positive Test Rate")
axs[1, 0].plot(state_date_list, state_pos_list, label="Positive Tests")
axs[1, 0].plot(state_date_list, state_neg_list, label="Negative Tests")
axs[1, 0].set_title("%s State COVID19 Test Rates" % selected_state)
axs[1, 1].plot(state_date_list, state_pos_rate)
axs[1, 1].set_title("%s State COVID19 Positive Test Rate" % selected_state)

for ax in axs.flat:
    ax.set(xlabel='Days', ylabel='Amount')

# Hide x labels and tick labels for top plots and y ticks for right plots
for ax in axs.flat:
    ax.label_outer()

plt.show()  
