import Adafruit_DHT
from ambient_api.ambientapi import AmbientAPI
from datetime import datetime, timedelta
from suntime import Sun
from skyfield import almanac
from skyfield.api import N, W, wgs84, load
import requests
import math
from pytz import timezone
from time import sleep

# API Keys and Constants
BREEZOMETER_API_KEY = 'YOUR_KEY_HERE'
LAT = 40.719499
LON = -73.935809

def getWeather():
    """
    Gets weather data from the Ambient Weather station.
    Returns: Dictionary containing weather data with descriptive keys.
    """
    api = AmbientAPI()
    devices = api.get_devices()
    device = devices[0]
    sleep(1)
    reports = device.get_data()
    report = reports[0]
    
    return {
        'indoor': {
            'temperature': report['tempinf'],
            'humidity': report['humidityin']
        },
        'outdoor': {
            'temperature': report['tempf'],
            'humidity': report['humidity']
        },
        'wind': {
            'direction': report['winddir'],
            'speed': report['windspeedmph'],
            'gust': report['windgustmph']
        },
        'rain': {
            'hourly': report['hourlyrainin']
        },
        'solar': {
            'radiation': report['solarradiation'],
            'uv': report['uv']
        }
    }

def getAir(LAT, LON):
    """
    Fetches tree pollen index from Breezometer API for the specified latitude and longitude.
    Returns: Tree pollen index value or None if request fails.
    """
    URL_BREEZOMETER2 = "https://api.breezometer.com/pollen/v2/forecast/daily?"
    Number_of_Days = 1
    URL_BREEZOMETER2 += f"lat={LAT}&lon={LON}&key={BREEZOMETER_API_KEY}&days={Number_of_Days}"

    response = requests.get(URL_BREEZOMETER2)
    if response.status_code == 200:
        json_data = response.json()
        data = json_data['data'][0]
        tree_pollen_index = data['types']['tree']['index']['value']
        return tree_pollen_index
    else:
        print(f"Error: Unable to fetch pollen data (Status code: {response.status_code})")
        return None

def getWater():
    """
    Fetches current water level data from NOAA API.
    Returns: Current water height in metric units.
    """
    url = 'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=latest&station=8518750&product=one_minute_water_level&datum=mllw&units=metric&time_zone=gmt&application=web_services&format=json'
    r = requests.get(url)
    with r as json_data:
        json = json_data.json()
        data = (json['data'][0])
        height = data['v']
        return height

def getMoon():
    """
    Calculates current moon phase using current date.
    Returns: Moon phase value (0-29).
    """
    current_date = datetime.now()
    mDay = current_date.day
    mMonth = current_date.month
    mYear = current_date.year
    
    r = mYear % 100
    r %= 19
    if r > 9:
        r -= 19
    r = ((r * 11) % 30) + mMonth + mDay
    if mMonth < 3:
        r += 2
    s = 4 if mYear < 2000 else 8.3
    r -= s
    r = (math.floor(r + 0.5) % 30)
    moon_phase = r + 30 if r < 0 else r
    return moon_phase

def getSunset():
    """
    Calculates sunset time using skyfield library.
    Returns: Sunset time as string.
    """
    zone = timezone('US/Eastern')
    now = zone.localize(datetime.now())
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    next_midnight = midnight + timedelta(days=1)

    ts = load.timescale()
    t0 = ts.from_datetime(midnight)
    t1 = ts.from_datetime(next_midnight)
    eph = load('de421.bsp')
    bluffton = wgs84.latlon(40.8939 * N, 83.8917 * W)
    f = almanac.dark_twilight_day(eph, bluffton)
    times, events = almanac.find_discrete(t0, t1, f)

    previous_e = f(t0)
    for t, e in zip(times, events):
        tstr = str(t.astimezone(zone))[:16]
        return tstr

def getSeason():
    """
    Determines current season based on day of year.
    Returns: String indicating current season (SPRING, SUMMER, FALL, or WINTER).
    """
    doy = datetime.today().timetuple().tm_yday
    # "day of year" ranges for the northern hemisphere
    spring = range(80, 172)
    summer = range(172, 264)
    fall = range(264, 355)
    # winter = everything else

    if doy in spring:
        return 'SPRING'
    elif doy in summer:
        return 'SUMMER'
    elif doy in fall:
        return 'FALL'
    else:
        return 'WINTER'
