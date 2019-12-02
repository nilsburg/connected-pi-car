import config
import at
import mqtt_functions
def connect():
    at.send('AT+CNACT=1,APN','OK',1)
    at.send('AT+SMCONF=\"URL\",\"'+config.MQTT_HOST+'\",\"'+config.MQTT_PORT+'\"','OK',1)
    at.send('AT+SMCONF=\"KEEPTIME\",60','OK',1)
    at.send('AT+SMCONN','OK',1)
