#!/usr/bin/python

import sys
import Server
import SensorListener
import threading
import time
import argparse

# Create parser
parser = argparse.ArgumentParser()

# Add arguments to the parser
parser.add_argument("--port", type=int, help="Port on which the REST server is running")
parser.add_argument("--log", help="URL to which any logs will be sent. Useful for simualtions")
parser.add_argument("--frequency",  type=int, default=1, help="How often the data will be requested in seconds")
parser.add_argument("--heartrate",  help="URL of the heartrate sensor")

# Define global variables 
sensors_map = {
    'heartrate' : None,
    'activity' : None
}

if __name__ == '__main__':
    # Parse the arguments 
    args = parser.parse_args()

    # List of threads to start/stop
    sensors_threads = []
    
    # Read from arguments and set up this device
    port = int(args.port)
    log_url = str(args.log) 
    frequency = int(args.frequency) 
    heartrate_sensor_url = str(args.heartrate)

    # 
    print("Port: " + str(port))

    print("Logs will be sent to the URL via POST: " + str(log_url))
 
    print("Request frequency set to: " + str(frequency))
    print("Heartrate data requested from: " + str(frequency))

    # Adding thread for running REST server
    server = Server.Server(port)
    server.daemon = True
    sensors_threads.append(server)

    # Adding thread for gathering data from the heartrate sensor
    sensors_map['heartrate'] = heartrate_sensor_url
    heartrate_sensor = SensorListener.SensorListener(sensors_map['heartrate'], frequency, log_url)
    heartrate_sensor.daemon = True
    sensors_threads.append(heartrate_sensor)

    # TODO: Add activity tracker

    try:
        for t in sensors_threads:
            t.start()
        
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        print("Stopping threads")
        for t in sensors_threads:
            t.stop()
        sys.exit()