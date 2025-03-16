import requests

class ReadGlobal:
    def fetch_weather_data(self):
        # Logic to fetch weather data from an API
        response = requests.get("https://api.weather.com/data")
        return response.json()

    def fetch_air_quality_data(self):
        # Logic to fetch air quality data from an API
        response = requests.get("https://api.airquality.com/data")
        return response.json() 