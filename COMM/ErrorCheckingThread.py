'''module for the errorcheking thread'''
from queue import Queue,Event
from ... import EncryptorData
from threading import Thread


class ErrorCheckingThread(Thread):
    '''thread to perform the errorchecking operation'''
    def __init__(self,ecsocket):
        super.__init__(self)
        self.switch =Event()
        self.switch.clear()
        self.ecsocket = ecsocket
        
        

    def start(self):
        while not self.switch.is_set():

            pass


    def off(self):
        self.switch.set()
