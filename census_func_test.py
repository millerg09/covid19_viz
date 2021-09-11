import pandas as pd

globvar = 1

def census_func():
    global globvar
    globvar = 2
    print (globvar)

census_func()