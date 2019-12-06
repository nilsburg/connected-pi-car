import serial
import time
import signal


class AT:
    def __init__(self, config):
        self.serial = serial.Serial(config.SERIAL, config.BAUDRATE)
        self.serial.flushInput()

    def send(self, command, back, timeout):
        rec_buff = ''
        self.serial.write((command + '\r\n').encode())
        time.sleep(timeout)
        if self.serial.inWaiting():
            time.sleep(0.01)
            rec_buff = self.serial.read(self.serial.inWaiting())
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

    def watch(self, command, timeout, callback, interrupHandler):
        buffer = ''
        self.serial.write((command + '\r\n').encode())
        time.sleep(timeout)
        line = ''
        while True:
            bytes = self.serial.inWaiting()
            buffer = self.serial.read(bytes)
            line = line + buffer
            if "\n" in buffer:
                callback(line)
                split = line.split(",")
                line = ''
            signal.signal(signal.SIGINT, interrupHandler)

    def close(self):
        self.serial.close()
