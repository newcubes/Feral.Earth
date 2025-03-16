from skyfield.api import load, Topos
from skyfield.almanac import find_discrete, moon_phases

class ReadCelestial:
    def __init__(self):
        self.eph = self.load_ephemeride()

    def load_ephemeride(self):
        # Load the ephemeris file
        return load('de421.bsp')

    def sense_sunrise(self, latitude, longitude):
        ts = load.timescale()
        observer = Topos(latitude, longitude)
        t0 = ts.utc(2023, 1, 1)
        t1 = ts.utc(2023, 12, 31)
        f = almanac.sunrise_sunset(self.eph, observer)
        times, events = find_discrete(t0, t1, f)
        # Extract sunrise times
        sunrise_times = [time for time, event in zip(times, events) if event == 0]
        return sunrise_times

    def sense_sunset(self, latitude, longitude):
        ts = load.timescale()
        observer = Topos(latitude, longitude)
        t0 = ts.utc(2023, 1, 1)
        t1 = ts.utc(2023, 12, 31)
        f = almanac.sunrise_sunset(self.eph, observer)
        times, events = find_discrete(t0, t1, f)
        # Extract sunset times
        sunset_times = [time for time, event in zip(times, events) if event == 1]
        return sunset_times

    def sense_phase(self):
        ts = load.timescale()
        t = ts.now()
        phase = moon_phases(self.eph, t)
        return phase

    def sense_season(self):
        # Placeholder logic for determining the current season
        # Implement logic to calculate the current season based on date and location
        return "Winter"

    def get_solstice(self):
        # Placeholder logic for calculating the next solstice
        # Implement logic to determine the date of the next solstice
        return "2023-12-21"

    def sense_eclipse(self):
        # Placeholder logic for calculating the next eclipse
        # Implement logic to determine the date and type of the next eclipse
        return "Lunar Eclipse on 2023-11-08"

    def get_moon(self):
        # Placeholder logic for getting moon information
        # Implement logic to retrieve detailed moon information
        return "Full Moon"

    def get_sunset(self, latitude, longitude):
        # Placeholder logic for calculating sunset time
        # Implement logic to calculate sunset time based on location
        return "18:00" 