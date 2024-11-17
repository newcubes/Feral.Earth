import subprocess
from time import sleep

def whosHere(addresses):
    sleep(10)
    output = subprocess.check_output("sudo arp-scan -l", shell=True).decode()
    presence = []
    for addr in addresses:
        if addr in output:
            presence.append(1)
        else:
            presence.append(0)
    return presence