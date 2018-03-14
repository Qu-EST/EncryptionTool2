import EncryptorData
import socket
from COMM.networkthread import NetworkThread
from COMM.ErrorCheckingThread import ErrorCheckingThread
from queue import Queue

def listen():
    '''This method creates a server for the error cheking and the messenger '''
    encryptordata = EncryptorData.EncryptorData()
    encryptordata.myec_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    encryptordata.mymessenger_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    encryptordata.myec_server_socket.bind((socket.gethostname(), encryptordata.ECPORT))
    encryptordata.mymessenger_server_socket.bind((socket.gethostname(), encryptordata.MESSENGERPORT))
    encryptordata.myec_server_socket.listen(3)
    encryptordata.myec_server_socket.setblocking(0)
    
    encryptordata.mymessenger_server_socket.listen(3)
    encryptordata.mymessenger_server_socket.setblocking(0)
    encryptordata.inputs.extend([encryptordata.myec_server_socket, encryptordata.mymessenger_server_socket])
    encryptordata.networkthread = NetworkThread()
    encryptordata.networkthread.start()
        
        
        
def errorcheck(ip, qsource):
    '''connects to the given ip, starts the errorcheck thread'''
    all_data = EncryptorData.EncryptorData()
    
    conn= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((ip, all_data.ECPORT))
    all_data.receiveddict[conn]=Queue(0)
    all_data.inputs.append(conn)
    all_data.ecthread[conn]=ErrorCheckingThread(conn, qsource)
    all_data.ecthread[conn].start()
    
def connect_messenger(ip):
    all_data = EncryptorData.EncryptorData()
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((ip, all_data.MESSENGERPORT))
    
class message_obj():
    def __init__(self, key_id, enc_msg, hash):
        self.key_id = key_id
        self.enc_msg = enc_msg
        self.hash = hash
def messenger_init(msoc):
    alldata= EncryptorData.EncryptorData()
    alldata.displaymessage[msoc] = Queue(0)
    alldata.senddict[msoc] = Queue(0)
    alldata.receiveddict[msoc] = Queue(0)
    alldata.sent_raw_message[msoc] = Queue(0)
    alldata.received_raw_message[msoc] = Queue(0)
