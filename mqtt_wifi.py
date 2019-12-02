import config
import at
import mqtt_functions as mf
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

client = None


def connect():
    client = mqtt.Client()
    client.connect(config.MQTT_HOST, config.MQTT_PORT, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
    return client


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT")
    client.subscribe(config.MQTT_TOPIC)
    send("Connected to MQTT on WIFI MODE")


def on_message(client, userdata, msg):
    data = msg.payload.decode()
    if config.DEBUG == True:
        print("DEBUG|MQTT_MSG_IN|", data)
    mf.run(data, __name__)


def send(message):
    print("Sending message", message)
    publish.single(config.MQTT_TOPIC, message, hostname=config.MQTT_HOST)
