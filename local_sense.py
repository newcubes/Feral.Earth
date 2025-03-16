import subprocess
import threading
import time

class ReadLocal:
    def __init__(self):
        self.iphone_mac_address = "A8:81:7E:18:0A:80"
        self.model_name = "YourModelName"  # Replace with your specific model name

    def read_wireless(self):
        # Thread to run rtl_433
        def rtl_433_thread():
            try:
                with subprocess.Popen(
                    ["rtl_433", "-f", "915M", "-M", "level"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                ) as process:
                    for line in iter(process.stdout.readline, b''):
                        decoded_line = line.decode('utf-8').strip()
                        if self.model_name in decoded_line:
                            print(f"Decoded signal: {decoded_line}")
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