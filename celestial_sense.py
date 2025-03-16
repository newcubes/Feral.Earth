from skyfield.api import load
from skyfield.almanac import find_discrete, moon_phases
from datetime import datetime, timedelta
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
            sunrise = sun.get_local_sunrise_time()
            return self.ramp([sunrise], 1)  # 1 hour window
        except SunTimeException as e:
            print(f"Error calculating sunrise: {e}")
            return 0

    def sense_sunset(self):
        sun = Sun(self.latitude, self.longitude)
        try:
            sunset = sun.get_local_sunset_time()
            return self.ramp([sunset], 1)  # 1 hour window
        except SunTimeException as e:
            print(f"Error calculating sunset: {e}")
            return 0

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

    def sense_solstice(self):
        ts = load.timescale()
        now = ts.now()
        t1 = ts.utc(now.utc_datetime().year + 1, 1, 1)
        t, _ = almanac.find_discrete(now, t1, almanac.seasons(self.eph))
        return self.ramp(t, 28 * 24)  # 4 weeks window in hours

    def sense_eclipse(self):
        ts = load.timescale()
        now = ts.now()
        t1 = ts.utc(now.utc_datetime().year + 1, 1, 1)
        x, _, _ = eclipselib.lunar_eclipses(now, t1, self.eph)
        return self.ramp(x, 28 * 24)  # 4 weeks window in hours

    def get_data(self):
        return {
            "sunrise": self.sense_sunrise(),
            "sunset": self.sense_sunset(),
            "moon_phase": self.sense_phase(),
            "season": self.sense_season(),
            "solstice": self.sense_solstice(),
            "eclipse": self.sense_eclipse()
        }

    def ramp(self, event_times, window_hours):
        ts = load.timescale()
        now = ts.now()

        if not event_times:
            return 0

        future_events = []
        for event_time in event_times:
            if isinstance(event_time, datetime):
                delta_hours = (event_time - datetime.now()).total_seconds() / 3600
            else:
                delta_days = event_time - now
                delta_hours = delta_days * 24

            if delta_hours > 0:
                future_events.append(delta_hours)

        if not future_events:
            return 0

        delta_hours = min(future_events)

        if abs(delta_hours) > window_hours:
            return 0
        else:
            # Exponential ramp-up
            return 100 * (1 - (abs(delta_hours) / window_hours) ** 2)

# Example usage
if __name__ == "__main__":
    celestial_reader = ReadCelestial()
    data = celestial_reader.get_data()
    print(json.dumps(data, indent=2))