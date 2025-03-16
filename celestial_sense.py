from skyfield.api import load
from skyfield.almanac import find_discrete, moon_phases
from datetime import datetime
from suntime import Sun, SunTimeException
from skyfield import almanac, eclipselib
import json

class ReadCelestial:
    def __init__(self):
        self.eph = self.load_ephemeride()
        self.latitude = 40.687672
        self.longitude = -73.955498

    def load_ephemeride(self):
        return load('de421.bsp')

    def sense_sunrise(self):
        sun = Sun(self.latitude, self.longitude)
        try:
            return sun.get_local_sunrise_time().strftime('%Y-%m-%d %H:%M:%S')
        except SunTimeException as e:
            print(f"Error calculating sunrise: {e}")
            return "N/A"

    def sense_sunset(self):
        sun = Sun(self.latitude, self.longitude)
        try:
            return sun.get_local_sunset_time().strftime('%Y-%m-%d %H:%M:%S')
        except SunTimeException as e:
            print(f"Error calculating sunset: {e}")
            return "N/A"

    def sense_phase(self):
        ts = load.timescale()
        t = ts.now()
        phase = almanac.moon_phase(self.eph, t)
        return phase.degrees

    def sense_season(self):
        doy = datetime.today().timetuple().tm_yday
        if doy in range(80, 172):
            return 'SPRING'
        elif doy in range(172, 264):
            return 'SUMMER'
        elif doy in range(264, 355):
            return 'FALL'
        else:
            return 'WINTER'

    def calculate_intensity(self, event_times):
        ts = load.timescale()
        now = ts.now()
        for event_time in event_times:
            delta_days = (event_time - now).days
            if delta_days > 0:
                if delta_days > 30:
                    return 0
                elif delta_days <= 5:
                    return 100
                else:
                    return 100 * (1 - (delta_days - 5) / 25)
        return 0

    def get_solstice_intensity(self):
        ts = load.timescale()
        now = ts.now()
        t1 = ts.utc(now.utc_datetime().year + 1, 1, 1)
        t, _ = almanac.find_discrete(now, t1, almanac.seasons(self.eph))
        return self.calculate_intensity(t)

    def get_eclipse_intensity(self):
        ts = load.timescale()
        now = ts.now()
        t1 = ts.utc(now.utc_datetime().year + 1, 1, 1)
        x, _, _ = eclipselib.lunar_eclipses(now, t1, self.eph)
        return self.calculate_intensity(x)

    def get_data(self):
        return {
            "sunrise": self.sense_sunrise(),
            "sunset": self.sense_sunset(),
            "moon_phase": self.sense_phase(),
            "season": self.sense_season(),
            "next_solstice_intensity": self.get_solstice_intensity(),
            "next_eclipse_intensity": self.get_eclipse_intensity()
        }

# Example usage
if __name__ == "__main__":
    celestial_reader = ReadCelestial()
    data = celestial_reader.get_data()
    print(json.dumps(data, indent=2))