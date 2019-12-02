import config
import at
import gps
import mqtt_wifi
import mqtt_sim
import sys
import json


def run(data, mqtt_module):
    mqtt = sys.modules[mqtt_module]
    data = data.encode('utf-8')

    if config.DEBUG == True:
        print("MQTT CLASS", mqtt)
        print("running command", data)
    split = data.split("|")
    print(split)
    command = split[0]
    # params = split[1].split(";")
    # callback = split[2]
    if command == "locate":
        position = gps.get_position()
        if config.DEBUG == True:
            print("Sending Position", position)
        data = json.dumps(position)
        mqtt.send(data)
    else:
        if config.DEBUG == True:
            print("unknown command")
