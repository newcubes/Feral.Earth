# Feral.Earth
Backend to feral.earth

Data Collection:

API Requests: External data sources (like OpenWeatherMap, Breezometer, etc.) provide real-time ecological data, such as weather conditions, air quality, and environmental variables.
Sensors: Local sensors (such as temperature, humidity, and presence detection) feed additional data into the system.
Module: The almanac.py file (formerly sensor_data_collection.py) fetches this data from both APIs and sensors.
Data Logging and Storage:

All the collected data is logged into a SQLite database by the database.py module. This includes information like temperature, humidity, wind speed, air quality, presence status, and other ecological factors.
The logData function stores the data, while the displayData function allows you to visualize the contents of the database for troubleshooting or review.
Control Logic:

Presence Detection: The presence.py file (formerly presence_detection.py) checks for the presence of specific devices (using ARP scanning, for example). This could be used to control access to a website or system based on whether certain individuals are present or not.
Ecological State Evaluation: Based on the collected data, the backend could evaluate whether certain conditions are met (e.g., weather conditions, air quality thresholds, or time of day). These conditions could determine whether users are granted access to specific links or features on the website.
Data Processing and Monitoring:

The utilities.py module provides utility functions like calculating the Minute of the Day (MOD), determining the sunrise and sunset times, and interacting with external APIs (like Breezometer).
This data helps monitor the environmental conditions and could be used to set rules for controlling website access.
