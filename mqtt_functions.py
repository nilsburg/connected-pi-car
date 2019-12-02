import config
import at
import gps
import mqtt_wifi
import mqtt_sim
def ru_n(MQTT):
	pass
def run(data):
	data = data.encode('utf-8')
	print("running command",data)
	split = data.split("|")
	print(split)
	command = split[0]
	#params = split[1].split(";")
	#callback = split[2]
	#print(command,params,callback)
	if command == "locate":
		print("A")
		position = gps.get_position()
		print("B")
		print(MQTT)
		MQTT.send(position)
		print("Positio",position)
	else:
		print("unknown command")


