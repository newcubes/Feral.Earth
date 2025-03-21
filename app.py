from flask import Flask, jsonify
import sqlite3

DB_PATH = 'sense_data.db'

app = Flask(__name__)

def fetch_latest_data():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM SensorData ORDER BY timestamp DESC LIMIT 1')
        row = cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'timestamp': row[1],
                'local_data': row[2],
                'celestial_data': row[3]
            }
        return None

@app.route('/')
def home():
    return "Welcome to the Sense Data App!"

@app.route('/latest')
def latest_data():
    data = fetch_latest_data()
    if data:
        return jsonify(data)
    else:
        return jsonify({'error': 'No data available'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 