import sqlite3

# Define the database file path
dbname = '/home/pi/AWS/Room/AWSData3.db'

def logData(status, tempinf, humidityin, tempf, humidity, winddir, windspeedmph, windgustmph, hourlyrainin, solarradiation, uv, moon, season, twilight, mod, mtsr, mtss, tide):
    """
    Logs the provided data into the database.
    """
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()

    # Execute SQL statement to insert data into the database
    curs.execute("INSERT INTO AWSData3 VALUES(datetime('now'), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?))",
                 (status, tempinf, humidityin, tempf, humidity, winddir, windspeedmph, windgustmph, hourlyrainin, solarradiation, uv, moon, season, twilight, mod, mtsr, mtss, tide))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

def displayData():
    """
    Displays all data stored in the database.
    """
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()

    print("\nEntire database contents:\n")
    # Execute SQL statement to fetch all data
    for row in curs.execute("SELECT * FROM AWSData3"):
        print(row)

    # Close the connection
    conn.close()
