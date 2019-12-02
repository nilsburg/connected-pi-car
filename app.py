#!/usr/bin/python
# -*- coding:utf-8 -*-
import config
import gps
import mqtt_sim
import network_check
import mqtt_wifi
import mqtt_functions
position = gps.get_position()
MQTT = None
if config.wifi == True:
	print("WIFI MODE")
	MQTT = mqtt_wifi
else:
	print("GPRS MODE")
	MQTT = mqtt_sim
#MQTT.connect()
def lala(data):
	print("REC",data)
at.getStream("AT+CGNSTST=1",60,lala)
#mqtt_functions.run(MQTT)
