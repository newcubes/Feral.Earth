from datetime import datetime
from pytz import timezone
import requests

# Move the API keys to their own variables for easier management
BREEZOMETER_API_KEY = 'YOUR_KEY_HERE'  # Breezometer API key
OPENWEATHERMAP_API_KEY = 'YOUR_KEY_HERE'  # Replace with your OpenWeatherMap API key

def MOD():
    """
    Returns the minute of the day (MOD), calculated as the number of minutes since midnight.
    """
    now = datetime.now()
    return (now.hour * 60) + now.minute

def Rise_Set_Delta():
    """
    Calculates the time difference (in minutes) between the current time and the next sunrise and sunset times.
    Returns the deltas in minutes for sunrise and sunset.
    """
    # Latitude and Longitude for location
    latitude = 40.719499
    longitude = -73.935809

    zone = timezone('US/Eastern')
    now = zone.localize(datetime.now())
    tmrw = now + timedelta(days=1)
    sun = Sun(latitude, longitude)

    today_sr = sun.get_local_sunrise_time(tmrw)
    today_ss = sun.get_local_sunset_time()

    sr_delta = now - today_sr
    ss_delta = now - today_ss

    mod = (now.hour * 60) + now.minute
    mtss = abs(ss_delta.seconds / 60 - 1440)  # Ensure that the sunset delta does not exceed 60 minutes
    mtsr = abs(sr_delta.seconds / 60)  # Ensure that the sunrise delta does not exceed 60 minutes

    if mtss > 60:
        mtss = 60
    if mtsr > 60:
        mtsr = 60

    return mtsr, mtss

