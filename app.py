#!/usr/bin/python
# -*- coding:utf-8 -*-
import config
import gps
import mqtt_sim
import network_check
import mqtt_wifi
import mqtt_functions
import at
import sys
position = gps.get_position()
MQTT = None
if config.wifi == True:
    print("WIFI MODE")
    MQTT = mqtt_wifi
else:
    print("GPRS MODE")
    MQTT = mqtt_sim


# MQTT.connect()
def lala(data):
    print("REC", data)


def fn(string):
	print("DD",string)
def stopTst(sig,frame):
	print("Stop CGNSTST")
	at.send("AT+CGNSTST=0","OK",1)
	sys.exit(0)
gps.trackPosition(5,fn)
# mqtt_functions.run(MQTT)
