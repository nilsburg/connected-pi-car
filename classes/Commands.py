import json
import sys
import time


class Commands:
    def __init__(self, mqtt):
        self.config = mqtt.config
        self.device = mqtt.device
        self.mqtt = mqtt
        self.gps = mqtt.gps
        self.tracking = False

    def run(self, command):
        print("Running command " + command)
        if command == 'position':
            self.get_location()
        if command == 'track_on':
            self.track_on()
        if command == 'track_off':
            self.track_off()

    def track_on(self):
        self.tracking = True
        timer = 0
        limit = 1000
        t = Thread
        while self.tracking and timer < limit:
            print("Track", timer)
            timer = timer+1
            self.get_location()
            #time.sleep(1)

    def track_off(self):
        print("Stop tracking")
        self.tracking = False

    def get_location(self):
        location = self.gps.get_position()
        jsonStr = json.dumps(location)
        print("B", jsonStr, self.config.GPS_TOPIC, self.mqtt.wifi)
        self.mqtt.send(jsonStr, self.config.GPS_TOPIC)
