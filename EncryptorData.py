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
        self.receiver=""
        self.sender=""
        self.hasher=""
        self.send_data=Queue(0)
        self.received_data=Queue(0)
        self.encrypt_socket=""
        self.receivedprocessor=""
        self.messenger=""
        self.encryptor=""
        self.ui=""
        self.gpstime=""
        self.gps_reader=""
        self.sendprocessor=""
        self.inputs=[]
        self.outputs=[]
        self.senddict={}
        self.receiveddict={}
        self.loginserversocket=None
        self.mymessenger_server_socket = None
        self.myec_server_socket = None
        self.filelist = []
        self.files=None          # to fill the filename
        self.MESSENGERPORT = 5010
        self.ECPORT = 5015
        self.networkthread = None
        self.ecthread={}
        self.messengerthread={}
        
def listen():
        '''This method creates a server for the error cheking and the messenger '''
        encryptordata = EncryptorData()
        encryptordata.myec_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        encryptordata.mymessenger_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        encryptordata.myec_server_socket.bind((socket.gethostname(), encryptordata.ECPORT))
        encryptordata.mymessenger_server_socket.bind((socket.gethostname(), encryptordata.MESSENGERPORT))
        encryptordata.inputs.extend([encryptordata.myec_server_socket, encryptordata.mymessenger_server_socket])
        encryptordata.networkthread = NetworkThread()
        encryptordata.networkthread.start()
        
        
        
def errorcheck(ip, qsource):
    '''connects to the given ip, starts the errorcheck thread'''
    all_data = EncryptorData()
    
    conn= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((ip, all_data.ECPORT))
    ecthread[conn]=ErrorCheckingThread(conn, qsource)
    ecthread[conn].start()
