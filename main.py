from local_sense import ReadLocal
from global_sense import ReadGlobal
from celestial_sense import ReadCelestial
import sqlite3
from datetime import datetime
import logging
import time
import json

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
    local_reader = ReadLocal()
    while True:
        data = local_reader.get_data()
        print(json.dumps(data, indent=2))
        time.sleep(10)  # Run every 10 seconds

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}") 