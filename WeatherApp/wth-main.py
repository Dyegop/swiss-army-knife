"""
Script to do the following:
  -Reads the requested location from the command line
  -Downloads JSON weather data from OpenWeatherMap.org
  -Converts the string of JSON data to a Python data structure
  -Prints the weather for today and the next two days
"""

import requests
import time
import json
import sys


# Variables
open_weather_api = json.load(open("api_key.json", "r"))  # API key
t = 60                                                   # Refresh time in seconds


# Check input parameters and get location
if len(sys.argv) < 2:
    print('Usage OpenWeather.py: City_name, 2-letter_Country_code')
    sys.exit()
location = ' '.join(sys.argv[1:])


while True:
    try:
        # Download the JSON data from OpenWeatherMap.org's API
        url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&APPID={open_weather_api["API_key"]}'
        re = requests.get(url)

        # Check that a request is succesful
        re.raise_for_status()

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    # Uncomment to see the raw JSON text
    # print(re.text)

    # Load JSON data into a Python variable.
    weatherData = json.loads(re.text)

    # Get results
    w = dict(weatherData.get('weather')[0])
    print('Current weather in %s:' % location)
    print(f"{w['main']} - {w['description']}")
    print("Temperature: %.1fºC" % (float(weatherData['main']['temp'])-273.15))
    print("Feels like: %.1fºC" % (float(weatherData['main']['feels_like'])-273.15))
    print(f"Pressure: {weatherData['main']['pressure']}")
    print('\n')
    time.sleep(t)
