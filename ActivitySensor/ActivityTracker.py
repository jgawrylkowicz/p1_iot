#!/usr/bin/python

import falcon
import json
import requests
import datetime
import sys
from requests.exceptions import ConnectionError
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectTimeout
from waitress import serve
from json import dumps
from falcon.media.validators import jsonschema

path = '/activity'
port = None
proxy = None


class ActivityTracker(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200  # This is the default status
        device_info = {
            'type' : 'ActivityTracker',
            'paths' : {
                'post': path,
                'get' : path,
                'egde': proxy
            } 
        }
        resp.body = dumps(device_info)


    def on_post(self, req, resp):
        # TODO: add json schema for validation
        resp.status = falcon.HTTP_200
        resp.body = "OK"
        data = req.media
        json = dumps(data)
        try :
            r = requests.post(proxy, data=json, timeout=0.05)
            print("Sending to " + proxy + " -> " + str(json) + " -> " + str(r))
        except (ReadTimeout, ConnectTimeout):
            print("Sending to " + proxy + " -> TIMEOUT" )
            r = "No response"


print ('Number of arguments: ' + str(len(sys.argv)))
assert len(sys.argv) == 3, "Not enough arguments"

# settings for this device
port = int(sys.argv[1]) # e.g. 8000
proxy = str(sys.argv[2]) # e.g. 'http://127.0.0.1:7000/device0'

print ("Activity data can be sent to <ip>:" + str(port) + str(path))
print ("Forwarding data to edge device on: " + str(proxy))

assert path != None, "The path is not set"
assert proxy != None, "Edge device is not set"
assert port > 0 and port <= 9000, "Port is not set"

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
activity = ActivityTracker()

# things will handle all requests to the '/things' URL path
app.add_route(path, activity)

serve(app, host="0.0.0.0", port=port)
