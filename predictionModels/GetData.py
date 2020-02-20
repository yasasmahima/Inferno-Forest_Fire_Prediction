import os
import time
from collections import namedtuple
from datetime import datetime, timedelta

import requests
from pyprind import ProgBar

location = '30.578806,-97.853065'

API = os.environ.get('9b5690662c5b7fedd69282b17c0f2d3d')
URL = 'https://api.darksky.net/forecast/9b5690662c5b7fedd69282b17c0f2d3d/30.578806,-97.853065'


# Attributes needed
features = [
    'date',
    'temperatureMean',
    'humidity',
    'temperatureMax',
    'temperatureMin',
    'widSpeed'
]

Daily_Weather = namedtuple('DailySummary', features)

# Get Data From the API
def extract_weather_api(url, api_key, target_date, days):

    records = []
    progress_bar = ProgBar(days)

    for _ in range(days):
        request = URL.format(
            API, location, target_date.strftime('%Y-%m-%dT%H:%M:%S')
        )
        response = requests.get(request)

        # Check if the api connected to the application successfully
        
        if response.status_code == 200:

            # Calculate Mean Temperature in every day

            def get_mean_temp():
                total_temp = 0
                for i in range(len(hourlyData)):
                    try:
                        total_temp += hourlyData[i]['temperature']
                    except KeyError:
                        total_temp += hourlyData[i-1]['temperature']
                meanTemp = total_temp / 24
                return meanTemp

            dailyData = response.json()['daily']['data'][0]
            hourlyData = response.json()['hourly']['data']
            try:
                records.append(
                    Daily_Weather(
                        date=target_date,
                        temperatureMean=get_mean_temp(),
                        humidity=dailyData['humidity'],
                        temperatureMax=dailyData['temperatureMax'],
                        temperatureMin=dailyData['temperatureMin'],
                        widSpeed=dailyData['windSpeed']
                    )
                )
            except KeyError:
                records.append(
                    Daily_Weather(
                        date=target_date,
                        temperatureMean=get_mean_temp(),
                        humidity=dailyData['humidity'],
                        temperatureMax=dailyData['temperatureMax'],
                        temperatureMin=dailyData['temperatureMin'],
                        widSpeed=dailyData['windSpeed']
                    )
                )

        progress_bar.update()
        target_date += timedelta(days=1)

    print("Getting data Success")
    return records


def getTargetDate():

    current_date = datetime.now()
    target_date = current_date - timedelta(days=1000)
    return target_date


def derive_nth_day_feature(df, feature, N):
    nth_prior_measurements = df[feature].shift(periods=N)
    col_name = f'{feature}_{N}'
    df[col_name] = nth_prior_measurements



dte=getTargetDate()


print(extract_weather_api(API, URL, dte, 500))