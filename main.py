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

DB_PATH = 'sensedata.db'

def create_table():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS SensorData (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                local_data TEXT,
                celestial_data TEXT
            )
        ''')
        conn.commit()
    print("Database and table created successfully.")

def insert_data(local_data, celestial_data):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO SensorData (local_data, celestial_data)
            VALUES (?, ?)
        ''', (local_data, celestial_data))
        conn.commit()
    print("Data inserted successfully.")

def maintain_db_size():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM SensorData')
        count = cursor.fetchone()[0]
        if count > 1000:
            cursor.execute('DELETE FROM SensorData WHERE id IN (SELECT id FROM SensorData ORDER BY timestamp ASC LIMIT ?)', (count - 1000,))
            conn.commit()
    print("Database size maintained.")

def main():
    create_table()
    local_sense = ReadLocal()
    celestial_sense = ReadCelestial()

    while True:
        local_data = local_sense.get_data()
        celestial_data = celestial_sense.get_data()
        print(f"Local data: {local_data}")
        print(f"Celestial data: {celestial_data}")
        insert_data(str(local_data), str(celestial_data))
        maintain_db_size()
        time.sleep(60)  # Log data every minute

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}") 