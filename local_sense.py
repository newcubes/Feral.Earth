import subprocess
import threading
import time
import json

class ReadLocal:
    def __init__(self):
        self.iphone_mac_address = "6E:66:D3:86:C5:E9"
        self.model_name = "AWX"

    def read_wireless(self):
        # Thread to run rtl_433
        def rtl_433_thread():
            try:
                # Use the full path to rtl_433
                rtl_433_path = "/home/pi/rtl_433/build/src/rtl_433"  # Ensure this path is correct
                with subprocess.Popen(
                    [rtl_433_path, "-f", "915M", "-M", "level", "-M", "report_meta", "-Y", "autolevel", "-F", "json:-"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                ) as process:
                    for line in iter(process.stdout.readline, ''):
                        try:
                            data = json.loads(line)
                            # Extract and print relevant ecological data
                            temperature = data.get('temperature_C', 'N/A')
                            humidity = data.get('humidity', 'N/A')
                            wind_direction = data.get('wind_dir_deg', 'N/A')
                            wind_avg_intensity = data.get('wind_avg_m_s', 'N/A')
                            wind_max_intensity = data.get('wind_max_m_s', 'N/A')
                            rain = data.get('rain_mm', 'N/A')
                            uv = data.get('uv', 'N/A')

                            print(f"Temperature: {temperature} °C")
                            print(f"Humidity: {humidity} %")
                            print(f"Wind Direction: {wind_direction} °")
                            print(f"Wind Average Intensity: {wind_avg_intensity} m/s")
                            print(f"Wind Max Intensity: {wind_max_intensity} m/s")
                            print(f"Rain: {rain} mm")
                            print(f"UV: {uv}")
                            print("-" * 40)  # Separator for readability
                        except json.JSONDecodeError:
                            continue  # Ignore lines that cannot be parsed
            except Exception as e:
                print(f"Error running rtl_433: {e}")

        # Start the rtl_433 thread
        threading.Thread(target=rtl_433_thread, daemon=True).start()

    def read_presence(self):
        # Thread to run arp-scan
        def arp_scan_thread():
            try:
                while True:
                    # Specify the network interface explicitly
                    output = subprocess.check_output("sudo arp-scan -I wlan0 -l", shell=True)
                    output = output.decode()

                    # Debugging: Print the raw output
                    print("ARP-scan output:")
                    print(output)

                    # Check if the MAC address is in the output
                    if self.iphone_mac_address.lower() in output.lower():
                        print("AWX is home")
                    else:
                        print("AWX is not home")
                    time.sleep(60)  # Sleep to avoid continuous scanning
            except subprocess.CalledProcessError as e:
                print(f"Error scanning network: {e}")

        # Start the arp-scan thread
        threading.Thread(target=arp_scan_thread, daemon=True).start()

    def process_data(self, data):
        # Logic to process sensor data
        return data

# Example usage
if __name__ == "__main__":
    local_reader = ReadLocal()
    local_reader.read_wireless()
    local_reader.read_presence()

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...") 