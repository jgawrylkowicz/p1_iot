#!/usr/bin/python

import falcon
import datetime
import requests
from waitress import serve
import threading
from urllib3.exceptions import MaxRetryError
from requests.exceptions import ConnectionError


'''
Get simple info about the device
'''
class DeviceInfo(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = str("test")


'''
Test connectivity to the device using a static route
'''
class TestConnectivity(object):
    def on_post(self, req, resp):
            resp.status = falcon.HTTP_200  
            resp.body = "OK"

class Server(threading.Thread): 
    def __init__(self, port, log_url=None):
        self.port = port
        self.log_url = log_url
        self.app = falcon.API()
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()

    def run(self):
        message = "Starting server thread at port: " + str(self.port)
        self.log(message)

        # Resources are represented by long-lived class instances
        info = DeviceInfo()
        self.app.add_route("/info", info)

        test = TestConnectivity()
        self.app.add_route("/test", test)

        # setting up the static routes for heartrate and activity
        serve(self.app, host="0.0.0.0", port=self.port)
    
    def join(self):
        super().join()
    
    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def log(self, message):
        print(str(message))
        if not self.log_url:
            try: 
                requests.post(self.log_url, data=message, timeout=0.05)
            except (Exception, MaxRetryError, ConnectionError) as e:
                print("Could not contact the log server: " + str(e))


