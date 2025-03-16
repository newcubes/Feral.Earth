from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import sqlite3
from datetime import *
import math

# Retrieve data from database
def getData():
	conn=sqlite3.connect('/home/pi/AWS/Room/AWSData3.db')
	curs=conn.cursor()
	print(curs)
	for row in curs.execute("SELECT * FROM AWSData3 ORDER BY timestamp DESC LIMIT 1"):
		time = str(row[0])
		status = row[1]
		tempinf = row[2]
		humidityin = row[3]
		tempf = row[4]
		humidity = row[5]
		winddir = row[6]
		windspeedmph = row[7]
		windgustmph = row[8]
		hourlyrainin = row[9]
		solarradiation = row[10]
		uv = row[11]
		moon = row[12]
		season = row[13]
		sunrise = row[14]
		mod = row[15]
		mtsr = row[16]
		mtss = row[17]
		pollen = row[18]
	conn.close()
	return time, status, tempinf, humidityin, tempf, humidity, winddir, windspeedmph, windgustmph, hourlyrainin, solarradiation, uv, moon,season, sunrise,mod,mtsr,mtss,pollen

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# main route
@app.route("/")
def index():


	time, status, tempinf, humidityin, tempf, humidity, winddir, windspeedmph, windgustmph, hourlyrainin, solarradiation, uv, moon, season, sunrise,mod,mtsr,mtss,pollen = getData()
	templateData = {
		'time': time,
		'status' : status,
		'tempinf' : tempinf,
		'humidityin' : humidityin,
		'tempf' : tempf,
		'humidity' : humidity,
		'winddir' : winddir,
		'windspeedmph' : windspeedmph,
		'windgustmph' : windgustmph,
		'hourlyrainin' : hourlyrainin,
		'solarradiation' : solarradiation,
		'uv' : uv,
		'moon' : moon,
		'season' : season,
		'sunrise' : sunrise,
        'mod' : mod,
		'mtsr' : mtsr,
		'mtss' : mtss,
		'pollen' : pollen
	}
	return render_template('index.html', **templateData)


@app.route('/api', methods=['GET'])
def api_all():
    conn = sqlite3.connect('/home/pi/AWS/Room/AWSData3.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM AWSData3;').fetchall()
    # AWS_room = all_books + "lunar: /br solar: br"
    return jsonify(all_books)




if __name__ == "__main__":
   app.run(host='0.0.0.0', port=6000, debug=False)
