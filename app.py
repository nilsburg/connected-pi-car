#!/usr/bin/python
# -*- coding:utf-8 -*-
import config
import gps
import mqtt_sim
import network_check
import mqtt_wifi
import mqtt_functions
position = gps.get_position()
print("POS1",position)
#print("spliT",gps.parse(position))
MQTT = None
if config.wifi == True:
	print("WIFI MODE")
	MQTT = mqtt_wifi
else:
	print("GPRS MODE")
	MQTT = mqtt_sim
MQTT.connect()
MQTT.run(MQTT)
