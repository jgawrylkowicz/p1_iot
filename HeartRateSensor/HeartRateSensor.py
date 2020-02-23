#!/usr/bin/python

import falcon
import json
import requests
import datetime
from requests.exceptions import ConnectionError
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectTimeout
from urllib3.exceptions import MaxRetryError
from waitress import serve
from json import dumps
from falcon.media.validators import jsonschema
import random
import argparse

# Create parser
parser = argparse.ArgumentParser()

# Add arguments to the parser
parser.add_argument("--port", type=int, help="Port on which the REST server is running")

# Define global variables
sensor_path = '/heartrate'
info_path = '/'
port = None

class DeviceInfo(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200  # This is the default status
        device_info = {
            'type' : 'HeartRateSensor',
            'paths' : {
                'get': sensor_path,
                'info' : info_path    
            }
        }
        resp.body = dumps(device_info)


class HeartRateSensor(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200  # This is the default status
        message = "Heartrate data requested from " + str(port)
 
        device_info = {
            'type' : 'HeartRateSensor',
            'bpm' : random.randrange(60, 70, 1),
            'time' : str(datetime.datetime.now())
        }
        resp.body = dumps(device_info)

        print(message)
    
# Parse the arguments 
args = parser.parse_args()

# Read from arguments and set up this device
port = int(args.port)
#log_url = str(args.log) 

print("BPM data can requested at: " + str(port) + str(sensor_path))
#print("Logs will be sent to the URL via POST: " + str(log_url))

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
heartrate = HeartRateSensor()
app.add_route(sensor_path, heartrate)

info = DeviceInfo()
app.add_route(info_path, info)

serve(app, host="0.0.0.0", port=port)
