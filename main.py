import pandas as pd

# Confirmed
confirmed_global = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
confirmed_global.drop("Province/State Lat Long".split(), axis=1, inplace=True)
confirmed_global = confirmed_global.groupby('Country/Region').sum()
confirmed_global = confirmed_global.unstack().reset_index()
confirmed_global.rename({'Country/Region': 'Country','level_0': 'Date', 0: 'Confirmed'}, axis=1, inplace=True)
confirmed = confirmed_global.reset_index().set_index(['Date', 'Country']).drop('index', axis=1)

# Deaths
deaths = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
deaths.drop("Province/State Lat Long".split(), axis=1, inplace=True)
deaths = deaths.groupby('Country/Region').sum()
deaths = deaths.unstack().reset_index()
deaths.rename({'Country/Region': 'Country','level_0': 'Date', 0: 'Deaths'}, axis=1, inplace=True)
deaths = deaths.reset_index().set_index(['Date', 'Country']).drop('index', axis=1)

# Join
df = confirmed.join(deaths)
df.reset_index(inplace=True)

# Fix US name
df.loc[df['Country'] == 'US', 'Country'] = 'United States'

# Save
df.to_csv("data/data.csv")