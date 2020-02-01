#!/usr/bin/python

import threading
import requests
import time
import json
from urllib3.exceptions import MaxRetryError
from requests.exceptions import ConnectionError

class SensorListener(threading.Thread): 
    def __init__(self, url, frequency, log_url):
        self.frequency = frequency
        self.url = url
        self.log_url = log_url
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()

    def run(self):
        print("Starting sensor listener at " + str(self.url))
        print("Sending logs to " + self.log_url)
        while True:
            resp = None
            if self.url: 
                try:
                    resp = requests.get(self.url, timeout=0.05)
                    print("Received data: " + json.dumps(resp.json()))
                except Exception as e:
                    print("Could not contact sensor at " + self.url + "( " + str(e) + " )" )
                
                if resp:
                    try:
                        requests.post(self.log_url, data=resp, timeout=0.05)
                        print("Sent logs to server")
                    except Exception as e:
                        print("Could not contact the log server (" + str(e) + ")")
           
            time.sleep(self.frequency)
                
    def join(self):
        super().join()
    
    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
