from flask import Flask, jsonify
from local_sense import LocalSense
from celestial_sense import CelestialSense

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Sense Data App!"

@app.route('/local')
def local_data():
    local_sense = LocalSense()
    data = local_sense.get_data()
    return jsonify(data)

@app.route('/celestial')
def celestial_data():
    celestial_sense = CelestialSense()
    data = celestial_sense.get_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 