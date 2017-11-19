'''This is a thread module, creates a listener thread, accepts connections, 
receives data, and transfers data'''
import EncryptorData
import select
import ErrorCheckingThread


class NetworkThread(Thread):
    def __init__(self):
        Thread.__init__()
        self.encryptordata = EncryptorData()
        self.inputs = self.encryptordata.inputs
        self.outputs = self.encryptordata.outputs
        self.senddict = self.encryptordata.senddict
        self.receiveddict = self.encryptordata.receiveddict
        self.switch = Event()
        self.switch.clear()

    def start(self):
        '''the following will be called when the thread starts'''
        while not self.switch.is_set():
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs)

            for s in readable:
                if s is self.encryptordata.loginserversocket:
                    pass
                    # parse the data and create appropriate data
                    # create the node frames/ delete the node frames.
                    
                else if s is self.encryptordata.myec_server_socket: 
                    conn, addr= s.accept()
                    self.encryptordata.inputs.extend([conn])
                    self.encryptordata.encryptorthread[conn]= ErrorCheckingThread.ErrorCheckingThread()
                    self.encryptordata.encryptorthread[conn].start()
                    pass
            
                    # accepts the connections
                    # create a errorchekgin thread
                else if s is self.encryptordata.mymessenger_server_socket:
                    conn, addr= s.accept()
                    pass
                    # accept the connections
                    #create a messengerthread
                
                else:
                    data = self.recv_msg(s)
                    self.encryptordata.receiveddict[s].put(data))
                #
                pass            # put in the queue.

            for s in writable:
                s.self.send_msg(s, self.senddict[s].get_nowait())
                self.outputs.remove(s)
            for s in exceptional:
                self.inputs.remove(s) # add the other code to remove the socket
                if s in self.outputs self.outputs.remove(s)
                s.close()
                del senddict[s]
                del receiveddict[s]
                
    def send_msg(sock, msg):
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg
        sock.sendall(msg)

    def recv_msg(sock):
        # Read message length and unpack it into an integer
        raw_msglen = recvall(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return recvall(sock, msglen)

    def recvall(sock, n):
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
