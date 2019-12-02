import config
import serial
import time
ser = serial.Serial(config.SERIAL,config.BAUDRATE)
ser.flushInput()

def send(command,back,timeout):                                                      
        rec_buff = ''                                                                   
        ser.write((command+'\r\n').encode())                                            
        time.sleep(timeout)                                                             
        if ser.inWaiting():                                                             
                time.sleep(0.01 )                                                       
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
def close():
    ser.close()
