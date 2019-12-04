#!/usr/bin/python
# -*- coding:utf-8 -*-
import config
import at
import time

pos = {'latitude': None, 'longitude': None, 'altitude': None, 'speed': None}
tracking=False

def power_on():
    print("Powering on GPS")
    at.send('AT+CGNSPWR=1', 'OK', 1)
    time.sleep(2)


def parse(data):
    data = data.encode('utf-8')
    split = data.split(",")
    pos['latitude'] = split[3]
    pos['longitude'] = split[4]
    pos['altitude'] = split[5]
    pos['speed'] = split[6]
    return pos


def get_position():
    rec_null = True
    answer = 0
    rec_buff = ''
    response = at.send('AT+CGNSINF', '+CGNSINF: ', 1)
    parsed = parse(response.decode())
    return parsed


def track(callback=None,frequency=1):
	while tracking:
		response = get_position()
		time.sleep(frequency)
		if callback:
			callback(response)
		else:
			print("trackPosition",response)


def track():
    power_on()
power_on()
