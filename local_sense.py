import subprocess
import threading
import time
import json

class ReadLocal:
    def __init__(self):
        self.iphone_mac_address = "6E:66:D3:86:C5:E9"
        self.model_name = "AWX"

    def read_wireless(self, duration=10):
        """Capture radio data for a specified duration and return the latest data."""
        rtl_433_path = "/home/pi/rtl_433/build/src/rtl_433"  # Ensure this path is correct
        latest_data = {}

        try:
            with subprocess.Popen(
                [rtl_433_path, "-f", "915M", "-M", "level", "-M", "report_meta", "-Y", "autolevel", "-F", "json:-"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            ) as process:
                start_time = time.time()
                while time.time() - start_time < duration:
                    line = process.stdout.readline()
                    if line:
                        try:
                            data = json.loads(line)
                            # Update latest data with new values
                            latest_data.update({
                                'temperature': data.get('temperature_C', 'N/A'),
                                'humidity': data.get('humidity', 'N/A'),
                                'wind_direction': data.get('wind_dir_deg', 'N/A'),
                                'wind_avg_intensity': data.get('wind_avg_m_s', 'N/A'),
                                'wind_max_intensity': data.get('wind_max_m_s', 'N/A'),
                                'rain': data.get('rain_mm', 'N/A'),
                                'uv': data.get('uv', 'N/A')
                            })
                        except json.JSONDecodeError:
                            continue  # Ignore lines that cannot be parsed
                process.terminate()  # Ensure the process is terminated
        except Exception as e:
            print(f"Error running rtl_433: {e}")

        return latest_data

    def read_presence(self):
        """Check if the iPhone is present on the network."""
        try:
            output = subprocess.check_output("sudo arp-scan -I wlan0 -l", shell=True)
            output = output.decode()

            # Check if the MAC address is in the output
            if self.iphone_mac_address.lower() in output.lower():
                return {"AWX": "home"}
            else:
                return {"AWX": "not home"}
        except subprocess.CalledProcessError as e:
            print(f"Error scanning network: {e}")
            return {"AWX": "error"}

    def get_data(self):
        """Get the latest data from all sensors."""
        wireless_data = {}
        presence_data = {}

        def fetch_wireless_data():
            nonlocal wireless_data
            wireless_data = self.read_wireless()

        def fetch_presence_data():
            nonlocal presence_data
            presence_data = self.read_presence()

        # Create threads
        wireless_thread = threading.Thread(target=fetch_wireless_data)
        presence_thread = threading.Thread(target=fetch_presence_data)

        # Start threads
        wireless_thread.start()
        presence_thread.start()

        # Wait for threads to complete
        wireless_thread.join()
        presence_thread.join()

        return {**wireless_data, **presence_data}

# Example usage
if __name__ == "__main__":
    local_reader = ReadLocal()
    data = local_reader.get_data()
    print(json.dumps(data, indent=2)) 