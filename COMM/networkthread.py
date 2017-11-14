'''This is a thread module, creates a listener thread, accepts connections, 
receives data, and transfers data'''
from ... import EncryptorData

class NetworkThread(Thread):
    def __init__(self):
        super.__init__()
        self.encryptordata = EncryptorData()
        self.switch = Event()
        self.switch.clear()

    def start(self):
        '''the following will be called when the thread starts'''
        while not self.switch.is_set():
            pass

    def off(self):
        '''this will be called to off the thread'''
        self.switch.set()
