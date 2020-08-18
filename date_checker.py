# check date of file
# Can you make it so python emails me when there's a new NYT dataset?
# or better yet, kick off the other plots jobs and send those as emails?
#https://stackoverflow.com/questions/22715086/scheduling-python-script-to-run-every-hour-accurately

# import your modules
from sys import argv
import os.path, time
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange)

# fetch NYT dataset
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
data = pd.read_csv(url, error_bad_lines=False)

# turn the read csv into a pandas DataFrame
df = pd.DataFrame(data)

# print the max date value
print (df['date'].max())

# print the entire dataframe filtered on the max value
# print df[df['date']==df['date'].max()]

# Current date time in local system
print(datetime.date(datetime.now()))


