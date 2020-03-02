import requests
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--url", "-u", help="Base url of the simulator")


def get_running_devices():
    response = requests.get(simulator_url + "/update")
    running_devices = response.json()
    print("Devices scheduled for update: " + str(len(running_devices)))
    return running_devices


def update_device(id, version, params):
    entry = {
        'version': version,
        'params': params
    }
    response = requests.post(simulator_url + "/devices/update/" + entry['version'], params=entry)
    print("Update of " + id + " : " + str(response))

    if response.status_code == 200:
        return True
    else:
        return False


args = parser.parse_args()
simulator_url = args.url
print("Simulator URL: " + simulator_url)

devices = get_running_devices()

if len(devices) == 0:
    print("No devices to update")
    sys.exit(-1)

update_states = []
for device in devices:
    state = update_device(device["deviceId"], device["version"], device["params"])
    update_states.append(state)

updated_devices = sum(update_states)

print(str(update_states) + " of " + str(len(update_states)) + " were updated.")

if updated_devices < len(devices):
    print(str(len(devices) - len(updated_devices)) + " device(s) could not be updated! ")
    sys.exit(-1)
else:
    print("All devices are updated! ")
    sys.exit(0)
