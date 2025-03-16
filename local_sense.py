import subprocess
import threading
import time
import json

class ReadLocal:
    def __init__(self):
        self.iphone_mac_address = "A8:81:7E:18:0A:80"
        self.model_name = "YourModelName"  # Replace with your specific model name

    def read_wireless(self):
        # Thread to run rtl_433
        def rtl_433_thread():
            try:
                # Use the full path to rtl_433
                rtl_433_path = "/home/pi/rtl_433/build/src/rtl_433"  # Replace with the actual path
                with subprocess.Popen(
                    [rtl_433_path, "-f", "915M", "-M", "level", "-M", "report_meta", "-Y", "autolevel", "-F", "json:-"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                ) as process:
                    for line in iter(process.stdout.readline, ''):
                        try:
                            data = json.loads(line)
                            if data.get('model') == "Fineoffset-WH24":
                                wind_speed = data.get('wind_avg_m_s', 0) * 2.23694  # Convert to MPH
                                wind_direction = data.get('wind_dir_deg', 0)  # Default to 0 if not found
                                print(f"Wind Speed: {wind_speed:.2f} MPH, Wind Direction: {wind_direction}°")
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
                    # Run the arp-scan command to find devices on the network
                    output = subprocess.check_output("sudo arp-scan -l", shell=True)
                    output = output.decode()

                    # Check if the MAC address is in the output
                    if self.iphone_mac_address in output:
                        print("iPhone is present")
                    else:
                        print("iPhone is not present")
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