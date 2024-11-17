from presence import whosHere
from almanac import getWeather, getSeason, getMoon, getSunset, getWater
from utilities import MOD, Rise_Set_Delta, breezometer_api_request
from database import logData, displayData
from time import sleep

occupant = ["AWS"]
address = ["A8:81:7E:18:0A:80"]

def main():
    while True:
        try:
            # Get presence data
            presence = whosHere(address)

            # Get weather data from almanac.py
            tempinf, humidityin, tempf, humidity, winddir, windspeedmph, windgustmph, air_quality_index, pollutants = getWeather()

            # Get other data
            season = getSeason()
            moonphase = getMoon()
            twilight = getSunset()
            mod = MOD()
            mtsr, mtss = Rise_Set_Delta()
            tide = getWater()

            # Log the data to the database
            logData(presence, tempinf, humidityin, tempf, humidity, winddir, windspeedmph, windgustmph, None, None, None, moonphase, season, twilight, mod, mtsr, mtss, tide)

            # Wait for 5 minutes before logging data again
            sleep(300)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()