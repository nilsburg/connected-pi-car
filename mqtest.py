import paho.mqtt.client as mqtt
import time


def on_connect(client, userdata, flags, rc):
    result, mid = client.subscribe("picar/#")
    client.publish("picar/main", "connected")

def on_message(client, userdata, msg):
    print(msg.payload)
    client.publish("picar/main", "hi")


client = mqtt.Client("picar")
client.on_connect = on_connect
client.on_message = on_message
client.connect("test.mosquitto.org")
client.loop_start()
while True:
    pass
