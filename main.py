# wearther: a Python program that tells you when you should switch to the right clothes for the weather :)
# uses open-meteo!

# pip install openmeteo-requests
# pip install requests-cache retry-requests numpy pandas

# initialisation, importing modules

import os
import json
from datetime import datetime
import requests
from dateutil import parser

# fixing invalid wearther.json file - if this occurs, will save original data and start over

defconf = { #defaults to Melbourne lat and long
            "lat": -37.8136,
            "long": 144.9631
        }
config = {}

def fixconfig():
    global config
    config = defconf # currently use default conf
    try:
        os.rename("wearther.json", "wearther-invalid.json")
    except Exception as e:
        print(e)
    with open("wearther.json", "w") as f:
        json.dump(defconf, f)
    

# checks weather

def mainweather():
    latitude = config["lat"]
    longitude = config["long"]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=apparent_temperature&timezone=auto&forecast_days=1"
    response = requests.get(url)

    weather = []
    high = []
    medium = []
    low = []
    verylow = []
    
    if response.status_code == 200:
        data = response.json()
        length = len(data['hourly']['time'])
        for i in range(length):
            weather.append((parser.parse(data['hourly']['time'][i]).strftime('%I%p').lower().lstrip('0'), data['hourly']['apparent_temperature'][i]))

        for i in weather: # TODO: high,mid,low,verylow parameters defined by config file
            if i[1] >= 30:
                high.append(i)
            elif 15 <= i[1] < 30:
                medium.append(i)
            elif 5 <= i[1] < 15:
                low.append(i)
            else:
                verylow.append(i)

        print("Weather today!")

        if high:
            print("High: ")
            for i in high:
                print("  " + i[0] + " " + str(i[1]) + "°C")
        if medium:
            print("Medium: ")
            for i in medium:
                print("  " + i[0] + " " + str(i[1]) + "°C")
        if low:
            print("Low: ")
            for i in low:
                print("  " + i[0] + " " + str(i[1]) + "°C")
        if verylow:
            print("Very low: ")
            for i in low:
                print("  " + i[0] + " " + str(i[1]) + "°C")

    else:
        print("Failed to get weather data", response.status_code)

# check if config file exists
configexist = False
if os.path.exists("wearther.json"):
    configexist = True

if configexist: #file exists
    with open("wearther.json", "r") as f:
        try:
            config = json.load(f)
            if config: # check file has content, i.e. {}. If file is empty, json will fail.
                # TODO: validate that config has lat, long in it!
                mainweather()
            else:
                fixconfig()
                mainweather()
        except json.decoder.JSONDecodeError:
            fixconfig()
            mainweather()
else: #file doesn't exist
    fixconfig()
    mainweather()
