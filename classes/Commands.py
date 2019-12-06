import json
import sys
import threading
import time

tracking = False


class Commands:
    def __init__(self, mqtt):
        self.config = mqtt.config
        self.device = mqtt.device
        self.mqtt = mqtt
        self.gps = mqtt.gps
        self.tracking = False
        self.track_thread = threading.Thread(target=self.track_on)

    def run(self, command):
        global tracking
        print("Running command " + command)
        if command == 'position':
            self.get_location()
        if command == 'track_on':
            tracking = True
            self.track_thread.start()
        if command == 'track_off':
            tracking = False
            self.track_off()

    def track_on(self):
        timer = 0
        print("Track start")
        while tracking:
            print("Track", timer, self.tracking)
            timer = timer + 1
            self.get_location()
            time.sleep(1)
        print("Track ended")

    def track_off(self):
        print("Stop tracking")
        self.track_thread.join()

    def get_location(self):
        location = self.gps.get_position()
        jsonStr = json.dumps(location)
        print("B", jsonStr, self.config.GPS_TOPIC, self.mqtt.wifi)
        self.mqtt.send(jsonStr, self.config.GPS_TOPIC)
