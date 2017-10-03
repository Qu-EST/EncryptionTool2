'''
Created on Apr 13, 2017

This class extends the Serial from the serial module
Used to read data from the TDC

Input: port number and the baudrate used for interfacing.
Operations:
1.Start reading
2.Stop reading
3.Read inherited from parent
4.Readline inherited from parent


@author: jee11
'''
from serial import Serial
import serial
class TDCReader(Serial):
    def __init__(self,port="COM3",baudrate=38400):
        '''constructor
        '''
        Serial.__init__(self)
        self.port=port
        self.baudrate=baudrate
        
        
    def change_baudrate(self,baudrate=38400):
        self.baudrate=baudrate
        
    def change_port(self,port="COM3"):
        self.port=port
       
    def start_TDC(self):
        self.open()
        print(self.is_open)
        print(self)
        
#         try:
#              
#         except serial.serialutil.SerialException as e:
#             print("no port with the following error exist. error:{}".format(e))
#         else:
#             print(self.is_open)
#             print(self)
        
    def stop_TDC(self):
        self.close()
        