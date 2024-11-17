import Adafruit_DHT
from ambient_api.ambientapi import AmbientAPI
from datetime import datetime
from suntime import Sun
from skyfield import api, almanac, load
import requests

def getDHTdata():
    DHT22Sensor = Adafruit_DHT.DHT11
    DHTpin = 16
    hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)
    if hum is not None and temp is not None:
        hum = round(hum)
        temp = round(temp, 1)
    return temp, hum

def getWeather():
    api = AmbientAPI()
    devices = api.get_devices()
    device = devices[0]
    sleep(1)
    reports = device.get_data()
    report = reports[0]
    return (report['tempinf'], report['humidityin'], report['tempf'], report['humidity'], 
            report['winddir'], report['windspeedmph'], report['windgustmph'], 
            report['hourlyrainin'], report['solarradiation'], report['uv'])

def getSeason():
    doy = datetime.today().timetuple().tm_yday
    if 80 <= doy < 172:
        return 'SPRING'
    elif 172 <= doy < 264:
        return 'SUMMER'
    elif 264 <= doy < 355:
        return 'FALL'
    else:
        return 'WINTER'

def getMoon():
    # Implement moon phase retrieval here
    pass

def getSunset():
    # Implement sunset time retrieval here
    pass

def getWater():
    # Implement water data retrieval here
    pass