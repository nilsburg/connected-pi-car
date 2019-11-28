#!/usr/bin/python

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import serial
import time

com_port = "25" # Change to match your config
baud_rate = 9600 # Change to match your config

#MQTT broker config
mqtt_host = "broker.hivemq.com"
mqtt_port = 1883
mqtt_topic = "picar/gps" #Change to whatever topic you want

ser = serial.Serial('/dev/ttyS'+com_port,baud_rate)
ser.flushInput()

power_key = 4
rec_buff = ''
rec_buff2 = ''
time_count = 0
def activateGPS():
	print("Activating GPS")
	send_at('AT+CGNSPWR=1','OK',1)
	time.sleep(2)
def send_at(command,back,timeout):
	rec_buff = ''
	ser.write((command+'\r\n').encode())
	time.sleep(timeout)
	if ser.inWaiting():
		time.sleep(0.01 )
		rec_buff = ser.read(ser.inWaiting())		
	if rec_buff != '':
		if back not in rec_buff.decode():
			print(command + ' ERROR')
			print(command + ' back:\t' + rec_buff.decode())
			return 0
		else:
			response = rec_buff.decode()
			return response
	else:
		print('GPS is not ready')
		return 0

def get_gps_position():
	response = ''
	print('Start GPS session...')
	rec_buff = ''
	activateGPS()
	response = send_at('AT+CGNSINF','+CGNSINF: ',1)
	split = response.split(",")	
	data = "RESP,"+split[3]+","+split[4]+","+split[5]+","+split[6]+","+split[7]
	print("SENDING DATA",data)
	publish.single(mqtt_topic, data, hostname=mqtt_host)
	
def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))  
  client.subscribe(mqtt_topic)
  print("Waiting for commands on "+mqtt_topic)

def on_message(client, userdata, msg):
	data = msg.payload.decode()
	split = data.split(",")
	if split[0] == 'GETPOS':
		print("Send position")      	
		try:
			get_gps_position()	
		except:
			print("Cant get pos")
			if ser != None:
				ser.close()

	#client.disconnect()
    
client = mqtt.Client()
client.connect(mqtt_host,mqtt_port,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
