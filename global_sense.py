import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ReadGlobal:
    def __init__(self):
        self.api_key_2 = os.getenv('API_KEY_2')
        self.api_key_3 = os.getenv('API_KEY_3')  # Assuming a separate key for tide data

    def sense_air_quality(self):
        # Ensure API keys are set
        if not self.api_key_2:
            raise ValueError("API_KEY_2 is not set. Please check your environment variables.")
        
        # Example API request using the key
        response = requests.get(f"https://api.airquality.com/data?apiKey={self.api_key_2}")
        return response.json()

    def sense_tides(self):
        if not self.api_key_3:
            raise ValueError("API_KEY_3 is not set. Please check your environment variables.")
        
        # Example API request for tide data
        response = requests.get(f"https://api.tides.com/data?apiKey={self.api_key_3}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching tide data: {response.status_code}")
            return {"error": "Failed to fetch tide data"}

# Example usage
if __name__ == "__main__":
    global_sense = ReadGlobal()
    air_quality_data = global_sense.sense_air_quality()
    tide_data = global_sense.sense_tides()
    print(air_quality_data)
    print(tide_data) 