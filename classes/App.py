from classes.AT import AT
from classes.AT_Test import AT_Test
from classes.GPS import GPS
from classes.Mqtt import Mqtt
import json
import time
import signal
import sys
import datetime


class App:
    def __init__(self, config):

        self.wifi = False
        self.config = config
        self.mqtt = None
        self.at = None
        self.gps = None

    def run(self):
        if self.config.MODE == 'test':
            print("Running AT Test mode")
            self.at = AT_Test(self.config)
        else:
            print("Running AT Serial mode")
            self.at = AT(self.config)
        self.gps = GPS(self.at)
        self.mqtt = Mqtt(self.config, self.at, self.gps)
        self.gps.power_on()
        signal.signal(signal.SIGINT, self.destroy)
        self.mqtt.connect()
        self.mqtt.client.loop_start()
        while True:
            if self.mqtt.connected:
                pass

    def destroy(self, sig, frame):
        print("Exiting")
        self.mqtt.send(self.date_string() + "|Manual exit", self.config.MAIN_TOPIC)
        self.mqtt.stop()
        sys.exit(0)

    @staticmethod
    def date_string():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
