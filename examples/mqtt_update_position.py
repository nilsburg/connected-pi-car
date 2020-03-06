
import sys
import serial
import os
import time
import re
from datetime import datetime
from paho.mqtt import client as mqtt
from base64 import b64encode, b64decode
from hashlib import sha256
from urllib import parse
from hmac import HMAC
#Reference: https://github.com/tmcadam/sim7000-tools

CMD_LINEBREAK = b'\r\n'
MQTT_URL="test.mosquitto.org"
MQTT_USERNAME=""
MQTT_PASSWORD=""
MQTT_TOPIC = 'mytopic'
PORT = "/dev/ttyS0"
BAUD = 9600
ser = serial.Serial(PORT, BAUD, timeout=1)
def send(data):
    ser.write(data)

def send_cmd(cmd):
    send(cmd.encode('utf-8') + CMD_LINEBREAK)

def watch(timeout=10, success=None, failure=None, echo_cmd=None):
    t_start = time.time()
    reply = list()
    while True:
        if ser.in_waiting:
            line = ser.readline()
            #Only require if using ser2net (serial over network)
            if line == b"\xff\xfb\x03\xff\xfb\x01\xff\xfe\x01\xff\xfd\x00\r\n" or b"ser2net" in line:
                continue
            line = line.decode('utf-8')
            echo = False
            if echo_cmd:
                echo = line.strip().endswith(echo_cmd)
            if line != CMD_LINEBREAK and not echo:
                line = line.strip()
                reply.append('\t' + line)
                if success and line.startswith(success):
                    return ("Success", reply, time.time()-t_start)
                if failure and line.startswith(failure):
                    return ("Error", reply, time.time()-t_start)
        if (time.time()-t_start) > timeout:
            return ("Timeout", reply, time.time()-t_start)
        time.sleep(0.02)

def AT(cmd="", timeout=10, success="OK", failure="+CME ERROR"):
    cmd = 'AT' + cmd
    print("----------- ", cmd, " -----------")
    send_cmd(cmd)
    reply = watch(echo_cmd=cmd, timeout=timeout, success=success, failure=failure)
    print("{0} ({1:.2f}secs):".format(reply[0], reply[2]))
    print(*reply[1], sep='\n')
    print('')
    return reply
def updatePosition():
    print("++++++++++++++++++++ MQTT - UPDATE POSITION +++++++++++++++++++++\n")
    AT("+CNACT=1") # Open wireless connection
    AT("+CNACT?") # Check connection open and have IP
    AT('+SMCONF="CLIENTID",1233')
    AT('+SMCONF="KEEPTIME",60') # Set the MQTT connection time (timeout?)
    AT('+SMCONF="CLEANSS",1')
    AT('+SMCONF="USERNAME","{}"'.format(MQTT_USERNAME))
    AT('+SMCONF="PASSWORD","{}"'.format(MQTT_PASSWORD))
    AT('+SMCONF="URL","{}","1883"'.format(MQTT_URL)) # Set MQTT address
    AT('+SMCONN', timeout=30)
    smstate = AT('+SMSTATE?') # Check MQTT connection state
    if smstate[1][0].split(":")[1].strip() == "0":
        AT('+SMCONN', timeout=30) # Connect to MQTT
    while(True):
        msg = getPosition()
        if msg:
            AT('+SMPUB="{}","{}",1,1'.format(MQTT_TOPIC,len(msg)), timeout=30, success=">") # Publish command
            send(msg.encode('utf-8'))
            watch(timeout=3)        
    AT('+SMDISC') # Disconnect MQTT
    AT("+CNACT=0") # Close wireless connection
def powerGPS():
    AT('+CGNSPWR=1', success='OK')

def getPosition():
    result = AT('+CGNSINF', success='+CGNSINF:')
    regex = r"CGNSINF: ([\w\d,\.\-]+)"
    if(result[0] == 'Success'):
        if isinstance(result[1], list):
            response = result[1][0]
            matches = re.finditer(r"\+CGNSINF: (.*)", response,re.M|re.I)
            for matchNumber, match in enumerate(matches, start=1):
                data = match.group(1)
                if data is not None:
                    cols = data.split(",")
                    if len(cols) == 22:
                        return data
    return None                
            
            

AT("", success="OK", timeout=30)
AT("+CMEE=2") # Set debug level
powerGPS()
updatePosition()

