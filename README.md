# Feral.Earth
Backend to feral.earth

## Overview

The backend system is composed of several modules that interact with external APIs, local sensors, and a database to monitor ecological conditions and control access based on predefined rules. The main functionalities of the system include:

- **Real-time Data Collection**: The system collects data from APIs (e.g., OpenWeatherMap, Breezometer) and local sensors (e.g., temperature, humidity, presence detection).
- **Data Logging**: All collected data is logged into a SQLite database for historical tracking and analysis.
- **Access Control Logic**: The system evaluates environmental conditions and device presence to control access to specific website links or pages.
- **Utility Functions**: Various utility functions to calculate time-based data and interact with external APIs.

## System Components

### 1. **Data Collection**:
   - **API Requests**: External data sources (like OpenWeatherMap, Breezometer) provide real-time ecological data, such as weather conditions, air quality, and environmental variables.
   - **Sensors**: Local sensors (such as temperature, humidity, and presence detection) feed additional data into the system.
   - **Module**: The **`almanac.py`** module fetches this data from both APIs and sensors.

### 2. **Data Logging and Storage**:
   - All the collected data is logged into an **SQLite database** by the **`database.py`** module. This includes information like temperature, humidity, wind speed, air quality, presence status, and other ecological factors.
   - The **`logData`** function stores the data, while the **`displayData`** function allows you to visualize the contents of the database for troubleshooting or review.

### 3. **Control Logic**:
   - **Presence Detection**: The **`presence.py`** module checks for the presence of specific devices (using ARP scanning, for example). This could be used to control access to a website or system based on whether certain individuals are present or not.
   - **Ecological State Evaluation**: Based on the collected data, the backend could evaluate whether certain conditions are met (e.g., weather conditions, air quality thresholds, or time of day). These conditions could determine whether users are granted access to specific links or features on the website.

### 4. **Data Processing and Monitoring**:
   - The **`utilities.py`** module provides utility functions like calculating the **Minute of the Day (MOD)**, determining the **sunrise and sunset times**, and interacting with external APIs (like Breezometer).
   - This data helps monitor the environmental conditions and could be used to set rules for controlling website access.

### 5. **Frontend Interaction**:
   - While the backend itself doesn't directly manage the website, it feeds real-time data into the frontend (likely through API calls or a WebSocket connection). Based on the ecological data and conditions, the frontend can update the user interface (UI) to show whether certain links or features are accessible.
