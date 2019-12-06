import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import datetime

from classes.Commands import Commands


class Mqtt:
    def __init__(self, config, device, gps):
        self.client_id = 'picar'
        self.gps = gps
        self.config = config
        self.wifi = config.wifi
        self.client = None
        self.device = device
        self.connected = False
        print("INIT MQTT")

    def connect(self):
        if self.wifi:
            self.connect_wifi()

    def connect_wifi(self):
        self.client = mqtt.Client(self.client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        if not self.connected:
            print("Connecting")
            self.client.connect(self.config.MQTT_HOST)

    def on_publish(self, userdata, mid):
        print("Publihing")

    def stop(self):
        if self.connected:
            self.connected = False
            self.client.disconnect()
            self.client.loop_stop()

    def on_connect(self, client, userdata, flags, rc):
        self.connected = True
        print("Connected to MQTT:" + str(rc), self.config.COMMAND_TOPIC)
        result, mid = client.subscribe(self.config.COMMAND_TOPIC)
        if result == mqtt.MQTT_ERR_SUCCESS:
            self.send("Connected to MQTT on WIFI MODE", self.config.MAIN_TOPIC)
            pass
        else:
            print("ERROR SUBSCRIBING TO " + self.config.COMMAND_TOPIC)
            pass

    def on_message(self, client, userdata, msg):
        data = msg.payload.decode()
        commands = Commands(self)
        if self.config.DEBUG:
            print("DEBUG|MQTT_MSG_IN|", data, data.encode())
        commands.run(data)
        # mf.run(data, __name__)

    def send(self, message, topic=None):
        if not self.connected:
            print("Not connected, cant send")
            return False
        if topic is None:
            topic = self.config.MAIN_TOPIC

        print("Sending message", message, topic)
        if self.wifi:
            self.client.publish(topic, message)
        return True
