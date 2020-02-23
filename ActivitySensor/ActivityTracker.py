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
sensor_path = '/activity'
info_path = '/'
port = None

class DeviceInfo(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200  # This is the default status
        device_info = {
            'type' : 'ActivityTracker',
            'paths' : {
                'get': sensor_path,
                'info' : info_path    
            }
        }
        resp.body = dumps(device_info)


class ActivityTracker(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200  # This is the default status
        message = "Activity requested from " + str(port)
 
        device_info = {
            'type' : 'ActivityTracker',
            'steps' : random.randrange(0, 5, 1),
            'time' : str(datetime.datetime.now())
        }
        resp.body = dumps(device_info)

        print(message)
    
# Parse the arguments 
args = parser.parse_args()

# Read from arguments and set up this device
port = int(args.port)

print("Activity data can requested at: " + str(port) + str(sensor_path))

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
heartrate = ActivityTracker()
app.add_route(sensor_path, heartrate)

info = DeviceInfo()
app.add_route(info_path, info)

serve(app, host="0.0.0.0", port=port)
