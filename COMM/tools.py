import EncryptorData
import socket
from COMM.networkthread import NetworkThread
from COMM.ErrorCheckingThread import ErrorCheckingThread

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
    ecthread[conn]=ErrorCheckingThread(conn, qsource)
    ecthread[conn].start()
