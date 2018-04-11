'''This is a thread module, creates a listener thread, accepts connections, 
receives data, and transfers data'''
import EncryptorData
import select, pickle
from COMM import ErrorCheckingThread, tools
from COMM.Encryptor import Encryptor
from threading import Thread, Event
from queue import Queue
import struct
from UI.messenger import Messenger
from twofish import Twofish
import datetime
class NetworkThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.encryptordata = EncryptorData.EncryptorData()
        self.inputs = self.encryptordata.inputs
        self.outputs = self.encryptordata.outputs
        self.senddict = self.encryptordata.senddict
        self.receiveddict = self.encryptordata.receiveddict
        self.switch = Event()
        self.switch.clear()
        print("inthe network thread")
        print(self.inputs)
        self.encryptor = Encryptor(b'7744')

    def run(self):
        '''the following will be called when the thread starts'''
        while not self.switch.is_set():
            #print("in networkthread while")
            #print(self.inputs)
            readable, writable, exceptional = select.select(self.encryptordata.inputs, self.encryptordata.outputs, self.encryptordata.inputs, 1)
            #print("after select")
            #print("printing the readables {}".format(readable))
            for s in readable:
                
                if s is self.encryptordata.loginserversocket:
                    pass
                    # parse the data and create appropriate data
                    # create the node frames/ delete the node frames.
                    
                elif s is self.encryptordata.myec_server_socket: 
                    conn, addr= s.accept()
                    print("connected to")
                    print(conn)
                    self.encryptordata.inputs.extend([conn])
                    conn.setblocking(0)
                    self.encryptordata.receiveddict[conn]=Queue(0)
                    self.encryptordata.encryptorthread[conn]= ErrorCheckingThread.ErrorCheckingThread(conn, False)
                    self.encryptordata.encryptorthread[conn].start()
                    pass
            
                    # accepts the connections
                    # create a errorchekgin thread
                elif s is self.encryptordata.mymessenger_server_socket:
                    def mess(conn):
                        self.messenger=Messenger(conn)
                        self.encryptordata.messenger=self.messenger
                        self.messenger.mainloop()
                    conn, addr= s.accept()
                    self.encryptordata.inputs.extend([conn])
                    conn.setblocking(0)
                    tools.messenger_init(conn)
                    mthread = Thread(target = mess, args = (conn,))
                    mthread.start()
                    
                    #call the messenger window
                    
                    pass
                    # accept the connections
                    #create a messengerthread
                
                else:
                    data = self.recv_msg(s)
                    socport = s.getsockname()[1]
                    peerport = s.getpeername()[1]
                    print(data)
                    self.encryptordata.receiveddict[s].put(data)
                    if ((socport == self.encryptordata.ECPORT) or (peerport==self.encryptordata.ECPORT)):
                        try:
                            if(self.encryptordata.ecthread[s].isalive()):
                                pass
                            else:
                                pass #create thread
                                self.encryptordata.ecthread[s]=ErrorCheckingThread(s, False)
                                self.encryptordata.ecthread.start()
                        except AttributeError:
                            pass
                            self.encryptordata.ecthread[s]=ErrorCheckingThread(s, False)
                            self.encryptordata.ecthread.start()
                    elif ((socport == self.encryptordata.MESSENGERPORT) or (peerport==self.encryptordata.MESSENGERPORT)):
                        data = pickle.loads(data)
                        key_id = data.key_id
                        enc_msg = data.enc_msg
                        key = self.encryptordata.key[key_id]
                        tfh=Twofish(key.encode())
                        msg = self.encryptor.decode(enc_msg, tfh)
                        self.encryptordata.received_raw_message[s].put("{} {}".format(key_id, enc_msg))
                        #decrypt
                        self.encryptordata.displaymessage[s].put(datetime.date.strftime(datetime.datetime.now(),'%m/%d-%H:%M:%S')+"\nBurchard: {}".format(msg.decode('utf-8')))

            for s in writable:
                print("inwritable")
                mesg = self.senddict[s].get_nowait()
                self.send_msg(s, mesg)
                
                self.outputs.remove(s)
            for s in exceptional:
                self.inputs.remove(s) # add the other code to remove the socket
                if s in self.outputs: self.outputs.remove(s)
                s.close()
                del senddict[s]
                del receiveddict[s]
        print("after while")
                
    def send_msg(self, sock, msg):
        # Prefix each message with a 4-byte length (network byte order)
        print(len(msg))
        msg = struct.pack('>I', len(msg)) + msg
        sock.sendall(msg)

    def recv_msg(self, sock):
        # Read message length and unpack it into an integer
        raw_msglen = self.recvall(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(sock, msglen)

    def recvall(self, sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data
        

    def off(self):
        '''this will be called to off the thread'''
        self.switch.set()
