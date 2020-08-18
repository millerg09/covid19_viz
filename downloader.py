import pandas as pd

url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
data = pd.read_csv(url, error_bad_lines=False)
data.to_csv('nyt_covid19.csv')