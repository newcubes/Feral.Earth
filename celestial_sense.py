from skyfield.api import load, Topos
from skyfield.almanac import find_discrete, moon_phases
from datetime import datetime, timedelta
from pytz import timezone
from suntime import Sun, SunTimeException
from skyfield import almanac, api, eclipselib
import json

class ReadCelestial:
    def __init__(self):
        self.eph = self.load_ephemeride()
        self.latitude = 40.687672
        self.longitude = -73.955498

    def load_ephemeride(self):
        # Load the ephemeris file
        return load('de421.bsp')

    def sense_sunrise(self, latitude=None, longitude=None):
        latitude = latitude if latitude is not None else self.latitude
        longitude = longitude if longitude is not None else self.longitude
        sun = Sun(latitude, longitude)
        try:
            sunrise = sun.get_local_sunrise_time()
            return sunrise
        except SunTimeException as e:
            print(f"Error calculating sunrise: {e}")
            return None

    def sense_sunset(self, latitude=None, longitude=None):
        latitude = latitude if latitude is not None else self.latitude
        longitude = longitude if longitude is not None else self.longitude
        sun = Sun(latitude, longitude)
        try:
            sunset = sun.get_local_sunset_time()
            return sunset
        except SunTimeException as e:
            print(f"Error calculating sunset: {e}")
            return None

    def sense_phase(self):
        ts = load.timescale()
        t = ts.now()
        phase = almanac.moon_phase(self.eph, t)
        return phase.degrees

    def sense_season(self):
        doy = datetime.today().timetuple().tm_yday
        spring = range(80, 172)
        summer = range(172, 264)
        fall = range(264, 355)
        if doy in spring:
            return 'SPRING'
        elif doy in summer:
            return 'SUMMER'
        elif doy in fall:
            return 'FALL'
        else:
            return 'WINTER'

    def get_solstice(self):
        ts = load.timescale()
        now = ts.now()
        t1 = ts.utc(now.utc_datetime().year + 1, 1, 1)
        t, y = almanac.find_discrete(now, t1, almanac.seasons(self.eph))
        for ti in t:
            delta = ti - now
            if delta > 0:
                return ti.utc_strftime('%Y-%m-%d')
        return None

    def sense_eclipse(self):
        ts = load.timescale()
        t = ts.now()
        t1 = ts.utc(2025, 1, 1)
        x, y, details = eclipselib.lunar_eclipses(t, t1, self.eph)
        for ti in x:
            eclipse = ti - t
            if eclipse > 0:
                return ti.utc_strftime('%Y-%m-%d')
        return None

    def get_data(self):
        """Gather all celestial data and return as a dictionary."""
        data = {
            "sunrise": self.sense_sunrise().strftime('%Y-%m-%d %H:%M:%S') if self.sense_sunrise() else "N/A",
            "sunset": self.sense_sunset().strftime('%Y-%m-%d %H:%M:%S') if self.sense_sunset() else "N/A",
            "moon_phase": self.sense_phase(),
            "season": self.sense_season(),
            "next_solstice": self.get_solstice(),
            "next_eclipse": self.sense_eclipse()
        }
        return data

# Example usage
if __name__ == "__main__":
    celestial_reader = ReadCelestial()
    data = celestial_reader.get_data()
    print(json.dumps(data, indent=2))