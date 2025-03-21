
import subprocess
from time import sleep
from threading import Thread
import sqlite3
import Adafruit_DHT
import requests
from ambient_api.ambientapi import AmbientAPI
import time
import json
import skyfield
from datetime import *
import math
from pytz import timezone
from skyfield import almanac
from skyfield import api
from skyfield.api import N, W, wgs84, load
from suntime import Sun, SunTimeException
from skyfield import eclipselib



dbname='/home/pi/AWS/Room/AWSData3.db'


# Edit these for how many people/devices you want to track
occupant = ["AWS"]

# MAC addresses for our phones
address = ["A8:81:7E:18:0A:80"]


# Sleep once right when this script is called to give the Pi enough time
# to connect to the network
sleep(10)



# Function that checks for device presence
def whosHere(i):
    # 30 second pause to allow main thread to finish arp-scan and populate output
    sleep(10)

    if stop == True:
        print ("Exiting Thread")
        exit()
    else:
        pass
    # If a listed device address is present print and stream
    if address[i] in output:
#       print(occupant[i] + "'s device is connected to your network")
        status = 1
        print(status)
        return status
    else:
#       print(occupant[i] + "'s device is not present")
        status = 0
        print(status)
        return status


# get data from DHT sensor
def getDHTdata():
    DHT22Sensor = Adafruit_DHT.DHT11
    DHTpin = 16
    hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)
    if hum is not None and temp is not None:
        hum = round(hum)
        temp = round(temp, 1)
    return temp, hum

# get data from Weather Station
def getWeather():
    api = AmbientAPI()
    devices = api.get_devices()
    try:
        device = devices[0]
        print("I successfully connected to the station")
    except:
        print("Failed to discover Weather Station")
        pass
    sleep(1)
    reports = device.get_data()
    try:
        report = reports[0]
    except:
        pass
        print("Failed to generate report")
    windgustmph = report['windgustmph']
    tempinf = report['tempinf']
    winddir = report['winddir']
    humidity = report['humidity']
    windspeedmph = report['windspeedmph']
    hourlyrainin = report['hourlyrainin']
    solarradiation = report['solarradiation']
    uv = report['uv']
    humidityin = report['humidityin']
    tempf = report['tempf']

    return tempinf,humidityin,tempf,humidity,winddir,windspeedmph,windgustmph,hourlyrainin,solarradiation,uv

def getSolstice():
    ts = load.timescale()
    now = ts.now()

    eph = api.load('de421.bsp')

    t1 = ts.utc(2025, 1, 1)


    t, y = almanac.find_discrete(now, t1, almanac.seasons(eph))
    seasons = []

    for ti in t:
         delta = ti -  now
         if delta > 0:
              seasons.append(delta)
         else:
              pass
    print(seasons[0])
    return(seasons[0])

def getSeason():
        doy = datetime.today().timetuple().tm_yday
        # "day of year" ranges for the northern hemisphere
        spring = range(80, 172)
        summer = range(172, 264)
        fall = range(264, 355)
        # winter = everything else

        if doy in spring:
          season = 'SPRING'
        elif doy in summer:
          season = 'SUMMER'
        elif doy in fall:
          season = 'FALL'
        else:
          season = 'WINTER'
        return(season)

def MOD():
        a = datetime.now()
        mod = (a.hour*60)+a.minute
        return int(mod)


def Rise_Set_Delta():

    latitude = 40.719499
    longitude = -73.935809

    zone = timezone('US/Eastern')
    now = zone.localize(datetime.now())
    tmrw = now + timedelta(days=1)
    sun = Sun(latitude, longitude)

    today_sr = sun.get_local_sunrise_time(tmrw)
    today_ss = sun.get_local_sunset_time()

    sr_delta = now-today_sr
    ss_delta = now-today_ss

    mod = (now.hour*60)+now.minute
    mtss = abs(ss_delta.seconds/60 - 1440)
    mtsr = abs(sr_delta.seconds/60)

    if mtss > 60:
        mtss = 60
    else:
        pass
    if mtsr > 60:
        mtsr = 60
    else:
        pass
    print (mtss)
    return mtsr, mtss

def breezometer_api_request(LAT, LON):
    URL_BREEZOMETER2 = "https://api.breezometer.com/pollen/v2/forecast/daily?"
    API_KEY = '8d1690edc8774a77b68c3d5d0a2a6de1'
    Number_of_Days = 1
    URL_BREEZOMETER2 += "lat={lat}&lon={lon}&key={api_key}&days={Number_of_Days}".format(lat=LAT, lon=LON, api_key=API_KEY, Number_of_Days=Number_of_Days)

    with requests.get(URL_BREEZOMETER2) as json_data:
        json = json_data.json()
        data = (json['data'][0])
        types = data['types']['tree']['index']['value']
        return types

def getWater():
    r = requests.get('https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=latest&station=8518750&product=one_minute_water_level&datum=mllw&units=metric&time_zone=gmt&application=web_services&format=json')
    with r as json_data:
        json = json_data.json()
        data = (json['data'][0])
        height = data['v']
        return height

def getEclipse():
    ts = load.timescale()
    t = ts.now()
    eph = api.load('de421.bsp')

    t1 = ts.utc(2025, 1, 1)

    x, y, details = eclipselib.lunar_eclipses(t, t1, eph)

    for ti in x:
        eclipse = ti-t
        return eclipse





def getMoon():
    ts = load.timescale()
    t = ts.now()
    now = t.utc_jpl()
    eph = api.load('de421.bsp')
    phase = almanac.moon_phase(eph, t)
    return phase.degrees

def getSunset():
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
        # if previous_e < e:
            # print(tstr, ' ', almanac.TWILIGHTS[e], 'starts')
        # else:
            # print(tstr, ' ', almanac.TWILIGHTS[previous_e], 'ends')
        # previous_e = e




# log sensor data on database
def logData(status, tempinf, humidityin, tempf, humidity, winddir, windspeedmph, windgustmph, hourlyrainin, solarradiation, uv, moon, season, twilight,mod,mtsr,mtss,tide,eclipse,solstice):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    print("I connected with the db")
    curs.execute("INSERT INTO AWSData3 VALUES(datetime('now'), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?),(?), (?), (?), (?), (?),(?),(?),(?),(?),(?))", (status, tempinf, humidityin, tempf, humidity, winddir, windspeedmph, windgustmph, hourlyrainin, solarradiation, uv, moon, season, twilight,mod,mtsr,mtss,tide,eclipse,solstice))
    conn.commit()
    conn.close()

# # display database data
def displayData():
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    print ("\nEntire database contents:\n")
    for row in curs.execute("SELECT * FROM AWSdata3"):
        print (row)
    conn.close()


#def displayLastData():
#    conn = sqlite3.connect(dbname)
#    curs = conn.cursor()
#    print ("\nLast logged contents:\n")
#    for row in curs.execute(SELECT * FROM DHT_PRESENCE_data ORDER BY timestamp DESC LIMIT 1"):
#        print (row)
#    conn.close
#
# Main thread
def main():

    cur_date = datetime.now()
    day = cur_date.day
    month = cur_date.month
    year = cur_date.year

    while True:

        try:

            # Initialize a variable to trigger threads to exit when True
            global stop
            global status
            stop = False
            global output

            #Detect my Presence
            # Assign list of devices on the network to "output"
            test = subprocess.check_output("sudo arp-scan -l", shell=True)
            output = test.decode()
            # Wait 30 seconds between scans
            sleep(10)
            for i in range(len(occupant)):
                present = whosHere(i)

            #Get Temperature and Humidity Data
            #temp, hum = getDHTdata()

            #Get Weather Data
            tempinf, humidityin, tempf, humidity, winddir, windspeedmph, windgustmph, hourlyrainin, solarradiation, uv = getWeather()
            #Get Season Data
            season=getSeason()
            #Get Moon Status
            moonphase = getMoon()
            #Get Minute of Day
            mod = MOD()
            #Get Sunset
            twilight = getSunset()
            #Get Deltas to Sunrise and Sunset
            mtsr, mtss = Rise_Set_Delta()
            #Get Tide data
            tide = getWater()


            #Number of days til next eclipse
            eclipse = getEclipse()
            #The DOY var contains the number of days until the next solstice / equinox. THIS NEEDS TO BE UPDATED IN APP AND DB
            solstice = getSolstice()
            #Store Weather Data to Database
            logData(present, tempinf, humidityin, tempf, humidity, winddir, windspeedmph, windgustmph, hourlyrainin, solarradiation, uv, moonphase,season, twilight,mod,mtsr,mtss,tide,eclipse,solstice)
            print("I logged the data")
            #displayData()
            sleep(300)

        except:
            # On a keyboard interrupt signal threads to exit
            pass

main()




