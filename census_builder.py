
county_df = "raw county_df"
state_df = "raw state_df"

print (county_df)
print (state_df)

def census_build_county():
    import pandas as pd
    path = '/Users/gabriel.miller/Desktop/python/covid19/census/'
    county_file = 'county_pop.csv'
    county_filepath = (path + county_file)
    global county_df
    county_df = pd.read_csv(county_filepath, error_bad_lines=False, encoding='latin-1')
    print (county_df)
    print ("county_df success")
    return

def census_build_state():
    import pandas as pd
    path = '/Users/gabriel.miller/Desktop/python/covid19/census/'
    state_file = 'state_pop.csv'
    state_filepath = (path + state_file)
    global state_df
    state_df = pd.read_csv(state_filepath, error_bad_lines=False)

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

    ### JOIN the datasets togethers
    df_abbrev = pd.DataFrame(list(us_state_abbrev.items()), index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                                                    11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                                                                    21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                                                                    31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
                                                                    41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
                                                                    51, 52, 53, 54, 55, 56])

    df_abbrev.columns = ['state', 'abbrev']
    state_df = state_df.set_index('state').join(df_abbrev.set_index('state'))
    state_df = state_df.reset_index()
    us_filter = state_df['state'] != 'United States'
    state_df = state_df[us_filter]
    print (state_df)
    print ("state_df success")
    return

census_build_state()
print(state_df)

print ("\n\n\n\n\n")

census_build_county()
print(county_df)