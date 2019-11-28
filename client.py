#!/usr/bin/python

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

#MQTT broker config
mqtt_host = "broker.hivemq.com"
mqtt_port = 1883
mqtt_topic = "picar/gps" #Change to whatever topic you want


publish.single(mqtt_topic, "GETPOS", hostname=mqtt_host)
def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
  msg = msg.payload.decode()
  split = msg.split(",")
  if(split[0] == 'RESP'):
  	latitude = split[1]
  	longitude = split[2]
  	altitude = split[3]
  	speed = split[4]
  	print("LAT: "+latitude+"|LNG:"+longitude+"|ALTITUDE:"+altitude+"|SPEED:"+speed)
  	client.disconnect()
  print(msg.payload.decode())
    
client = mqtt.Client()
client.connect(mqtt_host)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
