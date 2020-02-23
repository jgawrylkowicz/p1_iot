import requests
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--url", "-u", help="Base url of the simulator")

simulator_url = "http://localhost:7002"

def get_running_devices():
    response = requests.get(simulator_url + "/devices")
    devices = response.json()
    print("Running devices: " + str(len(devices)))
    return devices

def update_device(deviceid):
    response = requests.post(simulator_url + "/devices/update/" + deviceid)
    print("Update of " + deviceId + " : " + str(response))


args = parser.parse_args()
simulator_url = args.url  
print ("Simulator URL: " + simulator_url)

devices = get_running_devices()
for device in devices:
    deviceId = device["deviceId"]
    update_device(deviceId)