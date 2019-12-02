import config
import serial
import time
import re
ser = serial.Serial(config.SERIAL, config.BAUDRATE)
ser.flushInput()


def send(command, back, timeout):
    rec_buff = ''
    ser.write((command + '\r\n').encode())
    time.sleep(timeout)
    if ser.inWaiting():
        time.sleep(0.01)
        rec_buff = ser.read(ser.inWaiting())
    if rec_buff != '':
        if back not in rec_buff.decode():
            print(command + ' ERROR')
            print(command + ' back:\t' + rec_buff.decode())
            return False
        else:
            response = rec_buff.decode()
            return response
    else:
        return False


def getStream(command, timeout, callback):
    buffer = ''
    ser.write((command + '\r\n').encode())
    time.sleep(timeout)
    row = 0
    limit = 5000
    line = ''
    line2 = ''
    while False:
        bytes = ser.inWaiting()
        buffer = ser.read(bytes)
	line = line+buffer
	if "\n" in buffer:
		#line = line.encode()
		#print("NEW LINE",line)
		split = line.split(",")
		#print(split)
		if split[0] == '$GNGGA':
			print(split)
		line = ''
	row = row+1
    #print(line.decode())
    ser.write(('AT+CGNSTST=0\r\n').encode())
    #ser.close()


def close():
    ser.close()
