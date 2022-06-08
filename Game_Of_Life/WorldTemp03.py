#!/usr/bin/env python

import requests
import pandas as pd
from dateutil import parser, rrule
from datetime import datetime, time, date
import time

def getRainfallData(station, day, month, year):
    """
    Function to return a data frame of minute-level weather data for a single Wunderground PWS station.
    
    Args:
        station (string): Station code from the Wunderground website
        day (int): Day of month for which data is requested
        month (int): Month for which data is requested
        year (int): Year for which data is requested
    
    Returns:
        Pandas Dataframe with weather data for specified station and date.
    """
    url = "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID={station}&day={day}&month={month}&year={year}&graphspan=day&format=1"
    full_url = url.format(station=station, day=day, month=month, year=year)
    # Request data from wunderground data
    response = requests.get(full_url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
    data = response.text
    # remove the excess <br> from the text data
    data = data.replace('<br>', '')
    # Convert to pandas dataframe (fails if issues with weather station)
    try:
        dataframe = pd.read_csv(io.StringIO(data), index_col=False)
        dataframe['station'] = station
    except Exception as e:
        print("Issue with date: {}-{}-{} for station {}".format(day,month,year, station))
        return None
    return dataframe
    
# Generate a list of all of the dates we want data for
start_date = "2015-01-01"
end_date = "2015-12-31"
start = parser.parse(start_date)
end = parser.parse(end_date)
dates = list(rrule.rrule(rrule.DAILY, dtstart=start, until=end))

# Create a list of stations here to download data for
stations = ["IDUBLINF3", "IDUBLINF2", "ICARRAIG2", "IGALWAYR2", "IBELFAST4", "ILONDON59", "IILEDEFR28"]
# Set a backoff time in seconds if a request fails
backoff_time = 10
data = {}

# Gather data for each station in turn and save to CSV.
for station in stations:
    print("Working on {}".format(station))
    data[station] = []
    for date in dates:
        # Print period status update messages
        if date.day % 10 == 0:
            print("Working on date: {} for station {}".format(date, station))
        done = False
        while done == False:
            try:
                weather_data = getRainfallData(station, date.day, date.month, date.year)
                done = True
            except ConnectionError as e:
                # May get rate limited by Wunderground.com, backoff if so.
                print("Got connection error on {}".format(date))
                print("Will retry in {} seconds".format(backoff_time))
                time.sleep(10)
        # Add each processed date to the overall data
        data[station].append(weather_data)
    # Finally combine all of the individual days and output to CSV for analysis.
    pd.concat(data[station]).to_csv("data/{}_weather.csv".format(station))

station = 'IEDINBUR6' # Edinburgh
data_raw = pd.read_csv('data/{}_weather.csv'.format(station))

# Give the variables some friendlier names and convert types as necessary.
data_raw['temp'] = data_raw['TemperatureC'].astype(float)
data_raw['rain'] = data_raw['HourlyPrecipMM'].astype(float)
data_raw['total_rain'] = data_raw['dailyrainMM'].astype(float)
data_raw['date'] = data_raw['DateUTC'].apply(parser.parse)
data_raw['humidity'] = data_raw['Humidity'].astype(float)
data_raw['wind_direction'] = data_raw['WindDirectionDegrees']
data_raw['wind'] = data_raw['WindSpeedKMH']

# Extract out only the data we need.
data = data_raw.loc[:, ['date', 'station', 'temp', 'rain', 'total_rain', 'humidity', 'wind']]
data = data[(data['date'] >= datetime(2015,1,1)) & (data['date'] <= datetime(2015,12,31))]

# There's an issue with some stations that record rainfall ~-2500 where data is missing.
if (data['rain'] < -500).sum() > 10:
    print("There's more than 10 messed up days for {}".format(station))
    
# remove the bad samples
data = data[data['rain'] > -500]

# Assign the "day" to every date entry
data['day'] = data['date'].apply(lambda x: x.date())

# Get the time, day, and hour of each timestamp in the dataset
data['time_of_day'] = data['date'].apply(lambda x: x.time())
data['day_of_week'] = data['date'].apply(lambda x: x.weekday())    
data['hour_of_day'] = data['time_of_day'].apply(lambda x: x.hour)
# Mark the month for each entry so we can look at monthly patterns
data['month'] = data['date'].apply(lambda x: x.month)

# Is each time stamp on a working day (Mon-Fri)
data['working_day'] = (data['day_of_week'] >= 0) & (data['day_of_week'] <= 4)

# Classify into morning or evening times (assuming travel between 8.15-9am and 5.15-6pm)
data['morning'] = (data['time_of_day'] >= time(8,15)) & (data['time_of_day'] <= time(9,0))
data['evening'] = (data['time_of_day'] >= time(17,15)) & (data['time_of_day'] <= time(18,0))

# If there's any rain at all, mark that!
data['raining'] = data['rain'] > 0.0

# You get wet cycling if its a working day, and its raining at the travel times!
data['get_wet_cycling'] = (data['working_day']) & ((data['morning'] & data['rain']) |
                                                   (data['evening'] & data['rain']))

# Looking at the working days only and create a daily data set of working days:
wet_cycling = data[data['working_day'] == True].groupby('day')['get_wet_cycling'].any()
wet_cycling = pd.DataFrame(wet_cycling).reset_index()

# Group by month for display - monthly data set for plots.
wet_cycling['month'] = wet_cycling['day'].apply(lambda x: x.month)
monthly = wet_cycling.groupby('month')['get_wet_cycling'].value_counts().reset_index()
monthly.rename(columns={"get_wet_cycling":"Rainy", 0:"Days"}, inplace=True)
monthly.replace({"Rainy": {True: "Wet", False:"Dry"}}, inplace=True)    
monthly['month_name'] = monthly['month'].apply(lambda x: calendar.month_abbr[x])

# Get aggregate stats for each day in the dataset on rain in general - for heatmaps.
rainy_days = data.groupby(['day']).agg({
        "rain": {"rain": lambda x: (x > 0.0).any(),
                 "rain_amount": "sum"},
        "total_rain": {"total_rain": "max"},
        "get_wet_cycling": {"get_wet_cycling": "any"}
        })    

# clean up the aggregated data to a more easily analysed set:
rainy_days.reset_index(drop=False, inplace=True) # remove the 'day' as the index
rainy_days.rename(columns={"":"date"}, inplace=True) # The old index column didn't have a name - add "date" as name
rainy_days.columns = rainy_days.columns.droplevel(level=0) # The aggregation left us with a multi-index
                                                           # Remove the top level of this index.
rainy_days['rain'] = rainy_days['rain'].astype(bool)       # Change the "rain" column to True/False values

# Add the number of rainy hours per day this to the rainy_days dataset.
temp = data.groupby(["day", "hour_of_day"])['raining'].any()
temp = temp.groupby(level=[0]).sum().reset_index()
temp.rename(columns={'raining': 'hours_raining'}, inplace=True)
temp['day'] = temp['day'].apply(lambda x: x.to_datetime().date())
rainy_days = rainy_days.merge(temp, left_on='date', right_on='day', how='left')
rainy_days.drop('day', axis=1, inplace=True)

print ("In the year, there were {} rainy days of {} at {}".format(rainy_days['rain'].sum(), len(rainy_days), station) )   
print ("It was wet while cycling {} working days of {} at {}".format(wet_cycling['get_wet_cycling'].sum(), 
                                                      len(wet_cycling),
                                                     station))
print ("You get wet cycling {} % of the time!!".format(wet_cycling['get_wet_cycling'].sum()*1.0*100/len(wet_cycling)))

# Looking at the working days only and create a daily data set of working days:
wet_cycling = data[data['working_day'] == True].groupby('day')['get_wet_cycling'].any()
wet_cycling = pd.DataFrame(wet_cycling).reset_index()

# Group by month for display - monthly data set for plots.
wet_cycling['month'] = wet_cycling['day'].apply(lambda x: x.month)
monthly = wet_cycling.groupby('month')['get_wet_cycling'].value_counts().reset_index()
monthly.rename(columns={"get_wet_cycling":"Rainy", 0:"Days"}, inplace=True)
monthly.replace({"Rainy": {True: "Wet", False:"Dry"}}, inplace=True)    
monthly['month_name'] = monthly['month'].apply(lambda x: calendar.month_abbr[x])

# Get aggregate stats for each day in the dataset on rain in general - for heatmaps.
rainy_days = data.groupby(['day']).agg({
        "rain": {"rain": lambda x: (x > 0.0).any(),
                 "rain_amount": "sum"},
        "total_rain": {"total_rain": "max"},
        "get_wet_cycling": {"get_wet_cycling": "any"}
        })    

# clean up the aggregated data to a more easily analysed set:
rainy_days.reset_index(drop=False, inplace=True) # remove the 'day' as the index
rainy_days.rename(columns={"":"date"}, inplace=True) # The old index column didn't have a name - add "date" as name
rainy_days.columns = rainy_days.columns.droplevel(level=0) # The aggregation left us with a multi-index
                                                           # Remove the top level of this index.
rainy_days['rain'] = rainy_days['rain'].astype(bool)       # Change the "rain" column to True/False values

# Add the number of rainy hours per day this to the rainy_days dataset.
temp = data.groupby(["day", "hour_of_day"])['raining'].any()
temp = temp.groupby(level=[0]).sum().reset_index()
temp.rename(columns={'raining': 'hours_raining'}, inplace=True)
temp['day'] = temp['day'].apply(lambda x: x.to_datetime().date())
rainy_days = rainy_days.merge(temp, left_on='date', right_on='day', how='left')
rainy_days.drop('day', axis=1, inplace=True)

print ("In the year, there were {} rainy days of {} at {}".format(rainy_days['rain'].sum(), len(rainy_days), station) )
print ("It was wet while cycling {} working days of {} at {}".format(wet_cycling['get_wet_cycling'].sum(), 
                                                      len(wet_cycling),
                                                     station))
print ("You get wet cycling {} % of the time!!".format(wet_cycling['get_wet_cycling'].sum()*1.0*100/len(wet_cycling)))

import calmap

temp = rainy_days.copy().set_index(pd.DatetimeIndex(analysis['rainy_days']['date']))
#temp.set_index('date', inplace=True)
fig, ax = calmap.calendarplot(temp['hours_raining'], fig_kws={"figsize":(15,4)})
plt.title("Hours raining")
fig, ax = calmap.calendarplot(temp['total_rain'], fig_kws={"figsize":(15,4)})
plt.title("Total Rainfall Daily")

temp[['get_wet_cycling', 'total_rain', 'hours_raining']].plot()

def analyse_station(data_raw, station):
    """
    Function to analyse weather data for a period from one weather station.
    
    Args:
        data_raw (pd.DataFrame): Pandas Dataframe made from CSV downloaded from wunderground.com
        station (String): Name of station being analysed (for comments)
    
    Returns:
        dict: Dictionary with analysis in keys:
            data: Processed and cleansed data
            monthly: Monthly aggregated statistics on rainfall etc.
            wet_cycling: Data on working days and whether you get wet or not commuting
            rainy_days: Daily total rainfall for each day in dataset.
    """
    # Give the variables some friendlier names and convert types as necessary.
    data_raw['temp'] = data_raw['TemperatureC'].astype(float)
    data_raw['rain'] = data_raw['HourlyPrecipMM'].astype(float)
    data_raw['total_rain'] = data_raw['dailyrainMM'].astype(float)
    data_raw['date'] = data_raw['DateUTC'].apply(parser.parse)
    data_raw['humidity'] = data_raw['Humidity'].astype(float)
    data_raw['wind_direction'] = data_raw['WindDirectionDegrees']
    data_raw['wind'] = data_raw['WindSpeedKMH']
    
    # Extract out only the data we need.
    data = data_raw.loc[:, ['date', 'station', 'temp', 'rain', 'total_rain', 'humidity', 'wind']]
    data = data[(data['date'] >= datetime(2015,1,1)) & (data['date'] <= datetime(2015,12,31))]
    
    # There's an issue with some stations that record rainfall ~-2500 where data is missing.
    if (data['rain'] < -500).sum() > 10:
        print("There's more than 10 messed up days for {}".format(station))
        
    # remove the bad samples
    data = data[data['rain'] > -500]

    # Assign the "day" to every date entry
    data['day'] = data['date'].apply(lambda x: x.date())

    # Get the time, day, and hour of each timestamp in the dataset
    data['time_of_day'] = data['date'].apply(lambda x: x.time())
    data['day_of_week'] = data['date'].apply(lambda x: x.weekday())    
    data['hour_of_day'] = data['time_of_day'].apply(lambda x: x.hour)
    # Mark the month for each entry so we can look at monthly patterns
    data['month'] = data['date'].apply(lambda x: x.month)

    # Is each time stamp on a working day (Mon-Fri)
    data['working_day'] = (data['day_of_week'] >= 0) & (data['day_of_week'] <= 4)

    # Classify into morning or evening times (assuming travel between 8.15-9am and 5.15-6pm)
    data['morning'] = (data['time_of_day'] >= time(8,15)) & (data['time_of_day'] <= time(9,0))
    data['evening'] = (data['time_of_day'] >= time(17,15)) & (data['time_of_day'] <= time(18,0))

    # If there's any rain at all, mark that!
    data['raining'] = data['rain'] > 0.0

    # You get wet cycling if its a working day, and its raining at the travel times!
    data['get_wet_cycling'] = (data['working_day']) & ((data['morning'] & data['rain']) |
                                                       (data['evening'] & data['rain']))
    # Looking at the working days only:
    wet_cycling = data[data['working_day'] == True].groupby('day')['get_wet_cycling'].any()
    wet_cycling = pd.DataFrame(wet_cycling).reset_index()
    
    # Group by month for display
    wet_cycling['month'] = wet_cycling['day'].apply(lambda x: x.month)
    monthly = wet_cycling.groupby('month')['get_wet_cycling'].value_counts().reset_index()
    monthly.rename(columns={"get_wet_cycling":"Rainy", 0:"Days"}, inplace=True)
    monthly.replace({"Rainy": {True: "Wet", False:"Dry"}}, inplace=True)    
    monthly['month_name'] = monthly['month'].apply(lambda x: calendar.month_abbr[x])
    
    # Get aggregate stats for each day in the dataset.
    rainy_days = data.groupby(['day']).agg({
            "rain": {"rain": lambda x: (x > 0.0).any(),
                     "rain_amount": "sum"},
            "total_rain": {"total_rain": "max"},
            "get_wet_cycling": {"get_wet_cycling": "any"}
            })    
    rainy_days.reset_index(drop=False, inplace=True)
    rainy_days.columns = rainy_days.columns.droplevel(level=0)
    rainy_days['rain'] = rainy_days['rain'].astype(bool)
    rainy_days.rename(columns={"":"date"}, inplace=True)               
    
    # Also get the number of hours per day where its raining, and add this to the rainy_days dataset.
    temp = data.groupby(["day", "hour_of_day"])['raining'].any()
    temp = temp.groupby(level=[0]).sum().reset_index()
    temp.rename(columns={'raining': 'hours_raining'}, inplace=True)
    temp['day'] = temp['day'].apply(lambda x: x.to_datetime().date())
    rainy_days = rainy_days.merge(temp, left_on='date', right_on='day', how='left')
    rainy_days.drop('day', axis=1, inplace=True)
    
    print ("In the year, there were {} rainy days of {} at {}".format(rainy_days['rain'].sum(), len(rainy_days), station)   ) 
    print ("It was wet while cycling {} working days of {} at {}".format(wet_cycling['get_wet_cycling'].sum(), 
                                                          len(wet_cycling),
                                                         station))
    print ("You get wet cycling {} % of the time!!".format(wet_cycling['get_wet_cycling'].sum()*1.0*100/len(wet_cycling)))

    return {"data":data, 'monthly':monthly, "wet_cycling":wet_cycling, 'rainy_days': rainy_days}


    # Load up each of the stations into memory.
stations = [
 ("IAMSTERD55", "Amsterdam"),
 ("IBCNORTH17", "Vancouver"),
 ("IBELFAST4", "Belfast"),
 ("IBERLINB54", "Berlin"),
 ("ICOGALWA4", "Galway"),
 ("ICOMUNID56", "Madrid"),
 ("IDUBLIND35", "Dublin"),
 ("ILAZIORO71", "Rome"),
 ("ILEDEFRA6", "Paris"),
 ("ILONDONL28", "London"),
 ("IMUNSTER11", "Cork"),
 ("INEWSOUT455", "Sydney"),
 ("ISOPAULO61", "Sao Paulo"),
 ("IWESTERN99", "Cape Town"),
 ("KCASANFR148", "San Francisco"),
 ("KNYBROOK40", "New York"),
 ("IRENFREW4", "Glasgow"),
 ("IENGLAND64", "Liverpool"),
 ('IEDINBUR6', 'Edinburgh')
]
data = []
for station in stations:
   weather = {}
   print ("Loading data for station: {}".format(station[1])
   weather['data'] = pd.DataFrame.from_csv("data/{}_weather.csv".format(station[0]))
   weather['station'] = station[0]
   weather['name'] = station[1]
   data.append(weather))
 
for ii in range(len(data)):
    print ("Processing data for {}".format(data[ii]['name']))
    data[ii]['result'] = analyse_station(data[ii]['data'], data[ii]['station'])
 
# Now extract the number of wet days, the number of wet cycling days, and the number of wet commutes for a single chart.
output = []
for ii in range(len(data)):
    temp = {
            "total_wet_days": data[ii]['result']['rainy_days']['rain'].sum(),
            "wet_commutes": data[ii]['result']['wet_cycling']['get_wet_cycling'].sum(),
            "commutes": len(data[ii]['result']['wet_cycling']),
            "city": data[ii]['name']
        }
    temp['percent_wet_commute'] = (temp['wet_commutes'] *1.0 / temp['commutes'])*100
    output.append(temp)
output = pd.DataFrame(output)


# Generate plot of percentage of wet commutes
plt.figure(figsize=(20,8))
sns.set_style("whitegrid")    # Set style for seaborn output
sns.set_context("notebook", font_scale=2)
sns.barplot(x="city", y="percent_wet_commute", data=output.sort_values('percent_wet_commute', ascending=False))
plt.xlabel("City")
plt.ylabel("Percentage of Wet Commutes (%)")
plt.suptitle("What percentage of your cycles to work do you need a raincoat?", y=1.05, fontsize=32)
plt.title("Based on Wundergroud.com weather data for 2015", fontsize=18)
plt.xticks(rotation=60)
plt.savefig("images/city_comparison_wet_commutes.png", bbox_inches='tight')



