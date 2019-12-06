import time


class GPS:
    def __init__(self, device):
        self.powered = False
        self.device = device
        self.tracking = False

    def power_on(self):
        if not self.powered:
            print("Powering on GPS")
            self.device.send('AT+CGNSPWR=1', 'OK', 1)
            time.sleep(1)
            self.powered = True

    @staticmethod
    def parse(data):
        split = data.split(",")
        pos = {'latitude': split[3], 'longitude': split[4], 'altitude': split[5], 'speed': split[6]}
        return pos

    def get_position(self):
        response = self.device.send('AT+CGNSINF', '+CGNSINF: ', 1)
        parsed = self.parse(response)
        return parsed
