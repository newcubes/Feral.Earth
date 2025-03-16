from local_sense import ReadLocal
from global_sense import ReadGlobal
from celestial_sense import ReadCelestial
import sqlite3
from datetime import datetime
import logging
import time

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataLogger:
    def __init__(self, db_path='almanac_log.db'):
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        try:
            # Create a database connection and table if it doesn't exist
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS SensorData (
                        timestamp TEXT,
                        temperature REAL,
                        humidity REAL,
                        presence INTEGER,
                        weather TEXT,
                        air_quality TEXT,
                        sunrise TEXT,
                        sunset TEXT,
                        moon_phase TEXT,
                        season TEXT,
                        eclipse TEXT
                    )
                ''')
                conn.commit()
            logging.info("Database setup completed successfully.")
        except sqlite3.Error as e:
            logging.error(f"Database setup error: {e}")

    def log_data(self, data):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO SensorData (timestamp, temperature, humidity, presence, weather, air_quality, sunrise, sunset, moon_phase, season, eclipse)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    datetime.now().isoformat(),
                    data['temperature'],
                    data['humidity'],
                    data['presence'],
                    data['weather'],
                    data['air_quality'],
                    data['sunrise'],
                    data['sunset'],
                    data['moon_phase'],
                    data['season'],
                    data['eclipse']
                ))
                conn.commit()
            logging.info("Data logged successfully.")
        except sqlite3.Error as e:
            logging.error(f"Error logging data: {e}")

def retry_on_failure(func, retries=3, delay=5):
    """Retry decorator for handling transient failures."""
    def wrapper(*args, **kwargs):
        for attempt in range(retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(delay)
                else:
                    logging.error(f"All attempts failed for {func.__name__}.")
                    return None
    return wrapper

@retry_on_failure
def fetch_weather_data(global_reader):
    return global_reader.fetch_weather_data()

@retry_on_failure
def fetch_air_quality_data(global_reader):
    return global_reader.fetch_air_quality_data()

def main():
    # Initialize sensor readers
    local_reader = ReadLocal()
    global_reader = ReadGlobal()
    celestial_reader = ReadCelestial()

    # Initialize logger
    logger = DataLogger()

    # Collect data
    local_data = local_reader.read_wireless()
    presence_data = local_reader.read_presence()
    weather_data = fetch_weather_data(global_reader)
    air_quality_data = fetch_air_quality_data(global_reader)
    sunrise_times = celestial_reader.sense_sunrise(40.7128, -74.0060)  # Example coordinates
    sunset_times = celestial_reader.sense_sunset(40.7128, -74.0060)
    moon_phase = celestial_reader.sense_phase()
    season = celestial_reader.sense_season()
    eclipse = celestial_reader.sense_eclipse()

    # Prepare data for logging
    data = {
        'temperature': local_data.get('temperature'),
        'humidity': local_data.get('humidity'),
        'presence': presence_data.get('presence'),
        'weather': weather_data,
        'air_quality': air_quality_data,
        'sunrise': sunrise_times[0] if sunrise_times else None,
        'sunset': sunset_times[0] if sunset_times else None,
        'moon_phase': moon_phase,
        'season': season,
        'eclipse': eclipse
    }

    # Log data
    logger.log_data(data)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}") 