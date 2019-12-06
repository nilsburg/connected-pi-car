class AT_Test:
    def __init__(self, config):
        self.config = config

    @staticmethod
    def send(command, response, timeout):
        if command == 'AT+CGNSPWR=1':
            return True
        if command == 'AT+CGNSINF':
            return "+CGNSINF: 1,1,20160501124254.000,47.199897,9.442750,473.500,0.35,36.8,1,,1.1,1.9,1.6,,13,7,,,39,,"
        return False
