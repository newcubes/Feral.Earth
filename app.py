from flask import Flask, jsonify
from local_sense import ReadLocal
from global_sense import ReadGlobal
from celestial_sense import ReadCelestial
import sqlite3

app = Flask(__name__)

# Initialize sensor readers
local_reader = ReadLocal()
global_reader = ReadGlobal()
celestial_reader = ReadCelestial()

# Database path
DB_PATH = 'almanac_log.db'

def fetch_latest_data():
    """Fetch the latest data from the database."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM SensorData ORDER BY timestamp DESC LIMIT 1')
            row = cursor.fetchone()
            if row:
                return {
                    'timestamp': row[0],
                    'temperature': row[1],
                    'humidity': row[2],
                    'presence': row[3],
                    'weather': row[4],
                    'air_quality': row[5],
                    'sunrise': row[6],
                    'sunset': row[7],
                    'moon_phase': row[8],
                    'season': row[9],
                    'eclipse': row[10]
                }
            else:
                return None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

@app.route('/')
def index():
    """Root route to provide a simple status message."""
    return jsonify({'message': 'Welcome to the API. Use /api/data or /api/sensors to access data.'})

@app.route('/api/data', methods=['GET'])
def get_data():
    """API endpoint to get the latest sensor data."""
    data = fetch_latest_data()
    if data:
        return jsonify(data)
    else:
        return jsonify({'error': 'No data available'}), 404

@app.route('/api/sensors', methods=['GET'])
def get_sensors():
    """API endpoint to get current sensor readings."""
    local_data = local_reader.read_wireless()
    presence_data = local_reader.read_presence()
    weather_data = global_reader.fetch_weather_data()
    air_quality_data = global_reader.fetch_air_quality_data()
    sunrise_times = celestial_reader.sense_sunrise(40.7128, -74.0060)  # Example coordinates
    sunset_times = celestial_reader.sense_sunset(40.7128, -74.0060)
    moon_phase = celestial_reader.sense_phase()
    season = celestial_reader.sense_season()
    eclipse = celestial_reader.sense_eclipse()

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
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 