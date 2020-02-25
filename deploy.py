import requests
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--url", "-u", help="Base url of the simulator")

def get_running_devices():
    response = requests.get(simulator_url + "/update")
    devices = response.json()
    print("Devices scheduled for update: " + str(len(devices)))
    return devices

def update_device(deviceid, version, params):
    entry = {
        'version': version,
        'params': params
    }
    response = requests.post(simulator_url + "/devices/update/" + deviceid,  params=entry)
    print("Update of " + deviceId + " : " + str(response))

args = parser.parse_args()
simulator_url = args.url  
print ("Simulator URL: " + simulator_url)

devices = get_running_devices()
for device in devices:
    deviceId = device["deviceId"]
    version = device["version"]
    params = device["params"]
    update_device(deviceId, version, params)