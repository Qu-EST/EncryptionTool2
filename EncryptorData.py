from queue import Queue
from queue import LifoQueue

class Singleton(type):
    '''Metaclass for the singleton'''
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class EncryptorData(metaclass=Singleton):
    '''
    Data to be shared with all the encryptor modules
    '''
    def __init__(self):
        '''constructor
        '''
        self.ut = Queue(0)
        self.good_ut = Queue(0)
        self.batchlist = {0:"file.csv"}
        self.node_list = []
        self.serversocket = None
        self.tdc_reader = ""
        self.hash_queue = Queue(0)
        self.save_data = Queue(0)
        self.hasher = ""
        self.goodkey = ""
        self.encrypt_key = "74"
        self.gps_reader = ""
        
