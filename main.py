import pandas as pd

# Confirmed
confirmed_global = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
confirmed_global.drop("Province/State Lat Long".split(), axis=1, inplace=True)
confirmed_global = confirmed_global.groupby('Country/Region').sum()
confirmed_global = confirmed_global.unstack().reset_index()
confirmed_global.rename({'Country/Region': 'Country','level_0': 'Date', 0: 'Total Confirmed'}, axis=1, inplace=True)
confirmed = confirmed_global.reset_index().set_index(['Date', 'Country']).drop('index', axis=1)

# Deaths
deaths = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
deaths.drop("Province/State Lat Long".split(), axis=1, inplace=True)
deaths = deaths.groupby('Country/Region').sum()
deaths = deaths.unstack().reset_index()
deaths.rename({'Country/Region': 'Country','level_0': 'Date', 0: 'Total Deaths'}, axis=1, inplace=True)
deaths = deaths.reset_index().set_index(['Date', 'Country']).drop('index', axis=1)

# Join
df = confirmed.join(deaths)
df.reset_index(inplace=True)

# Fix US name
df.loc[df['Country'] == 'US', 'Country'] = 'United States'

# Get Vaccination data
vac = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv")
vac['Date'] = vac['date'].apply(lambda d: pd.to_datetime(d).strftime("X%m/X%d/%y").replace('X0','X').replace('X',''))

# Fix Vaccination data
vac.rename(columns={
    'location': 'Country',
    'total_vaccinations': 'Total Vaccinations',
    'people_vaccinated': 'People Vaccinated',
    'people_fully_vaccinated': 'People Fully Vaccinated',
    'daily_vaccinations_raw': 'New Total Vaccinations',
    'people_vaccinated_per_hundred': 'People Vaccinated (per hundred)',
    'people_fully_vaccinated_per_hundred': 'People Fully Vaccinated (per hundred)',
    'daily_vaccinations_per_million': 'Daily Vaccinations (per million)',
}, inplace=True)
vac.drop(['daily_vaccinations','total_vaccinations_per_hundred','iso_code','date'],axis=1,inplace=True)

# Process data for each country
for country in df['Country'].unique():
    df.loc[df['Country'] == country, 'New Confirmed'] = df[df['Country'] == country]['Total Confirmed'] - df[df['Country'] == country]['Total Confirmed'].shift(1,fill_value = 0)
    df.loc[df['Country'] == country, 'New Deaths'] = df[df['Country'] == country]['Total Deaths'] - df[df['Country'] == country]['Total Deaths'].shift(1,fill_value = 0)
    
    df.loc[df['Country'] == country, 'Average Confirmed (7 days)'] = df[df['Country'] == country]['New Confirmed'].rolling(7).mean()
    df.loc[df['Country'] == country, 'Average Deaths (7 days)'] = df[df['Country'] == country]['New Deaths'].rolling(7).mean()
    
    df.loc[df['Country'] == country, 'Average Confirmed (14 days lag)'] = df[df['Country'] == country]['Average Confirmed (7 days)'].shift(14,fill_value = 0)
    df.loc[df['Country'] == country, 'Average Deaths (14 days lag)'] = df[df['Country'] == country]['Average Deaths (7 days)'].shift(14,fill_value = 0)
    
    vac.loc[vac['Country'] == country, 'New People Vaccinated'] = vac[vac['Country'] == country]['People Vaccinated'] - vac[vac['Country'] == country]['People Vaccinated'].shift(1)
    vac.loc[vac['Country'] == country, 'New People Fully Vaccinated'] = vac[vac['Country'] == country]['People Fully Vaccinated'] - vac[vac['Country'] == country]['People Fully Vaccinated'].shift(1)

# Join vaccination data
df = df.set_index(['Date','Country']).join(vac.set_index(['Date','Country'])).reset_index()
    
# Save
df.to_csv("data/country_daily.csv")

# Global data
df_global = df[['Date','Total Confirmed','Total Deaths', 'New Confirmed', 'New Deaths','Total Vaccinations', 'People Vaccinated', 'People Fully Vaccinated', 'New Total Vaccinations', 'New People Vaccinated', 'New People Fully Vaccinated']].groupby('Date').sum().reset_index()
df_global.to_csv("data/global_daily.csv")