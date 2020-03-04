import requests
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--url", "-u", help="Base url of the simulator")
parser.add_argument("--step", "-s", nargs='?', help="Define how many devices should be updated in a single step", required=False)
parser.add_argument("--force", "-f", nargs='?', type=bool,  help="Force stepwise update even with a low number of devices", required=False)


# Update maximum of 'step' amount of devices at the time.
# Check if the update was successful, fail the process if not.
def update_step_wise(devices, step):
    it = iter(devices)
    wave = 0
    num_of_updated_devices = 0
    try:
        while True:
            wave += 1
            print("Wave: " + str(wave))
            for x in range(step):
                device = next(it, None)
                if device is None:
                    raise StopIteration
                else:
                    if update_device(device["deviceId"], device["version"], device["params"]):
                        num_of_updated_devices += num_of_updated_devices + 1
                        print("Updated device: " + str(device["deviceId"]))
                    else:
                        raise RuntimeError("Update failed for " + str(device["deviceId"]))
    except StopIteration:
        print("No devices left!")
        pass
    except RuntimeError as e:
        print(e)
        not_updated_devices = len(devices) - num_of_updated_devices
        print(str(not_updated_devices) + " device(s) could not be updated! ")
        sys.exit(-1)

    print("All devices are updated! ")
    sys.exit(0)


# Update all at the same time
def update_simply(devices):
    #
    update_states = []
    for device in devices:
        state = update_device(device["deviceId"], device["version"], device["params"])
        update_states.append(state)

    num_of_updated_devices = sum(update_states)
    num_of_all_devices = len(devices)

    print(str(num_of_updated_devices) + " of " + str(num_of_all_devices) + " were updated.")

    if num_of_updated_devices < num_of_all_devices:
        not_updated_devices = num_of_all_devices - num_of_updated_devices

        print(str(not_updated_devices) + " device(s) could not be updated! ")
        sys.exit(-1)
    else:
        print("All devices are updated! ")
        sys.exit(0)


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
    response = requests.post(simulator_url + "/devices/update/" + id, params=entry)
    print("Update of " + id + " : " + str(response))

    if response.status_code == 200:
        return True
    else:
        return False


args = parser.parse_args()
simulator_url = args.url
step_size = args.step
is_step_wise = args.force

if is_step_wise and step_size == 0:
    step_size = 2
    print("Incorrect step size. Set to default of 2")

print("Simulator URL: " + simulator_url)
print("Step size: " + str(step_size))
print("Forced step-wise: " + str(is_step_wise))

devices = get_running_devices()
if len(devices) == 0:
    print("No devices to update")
    sys.exit(-1)

# different strategies depending on number of devices to be updated
if len(devices) > 5 or is_step_wise:
    update_step_wise(devices, step_size)
else:
    update_simply(devices)
