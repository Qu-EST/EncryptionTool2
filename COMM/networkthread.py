'''This is a thread module, creates a listener thread, accepts connections, 
receives data, and transfers data'''
import EncryptorData
import select

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
                else if s is (self.encryptordata.myec_server_socket or self.encryptordata.mymessenger_server_socket):
                    pass
                    # accepts the connections
                else
                self.encryptordata.receiveddict[s].put(s.recv())
                pass            # put in the queue.

            for s in writable:
                s.send(self.senddict[s].get_nowait())
                self.outputs.remove(s)
            for s in exceptional:
                self.inputs.remove(s) # add the other code to remove the socket
                if s in self.outputs self.outputs.remove(s)
                s.close()
                del senddict[s]
                del receiveddict[s]
                       

    def off(self):
        '''this will be called to off the thread'''
        self.switch.set()
