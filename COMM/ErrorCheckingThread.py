'''module for the errorcheking thread'''
from queue import Queue, Empty
import EncryptorData
from threading import Thread,Event
from COMM import ErrorChecking as e


class ErrorCheckingThread(Thread):
    '''thread to perform the errorchecking operation'''
    def __init__(self,ecsocket, qsource):
        Thread.__init__(self)
        self.switch =Event()
        self.switch.clear()
        self.ecsocket = ecsocket
        self.alldata=EncryptorData.EncryptorData()
        self.files=None
        self.qsource = qsource
        

    def run(self):
        if self.qsource:
            if not self.alldata.filelist:
                self.files = self.alldata.files
            else:
                self.files = self.alldata.filelist[-1]
            data = self.senddataproc("filename", self.files)
            self.alldata.senddict[ecsocket] = Queue(0)
            self.alldata.senddict[ecsocket].put(data)
        while not self.switch.is_set():
            try:
                receiveddata = self.alldata.receiveddict[self.ecsocket].get(timeout=1)
            except Empty:
                pass
            else:
                command, data = self.receiveddataproc(data)
                if(command is "filename"):
                    print("in file name block")
                    self.sdf = e.read_file_gps_coun(PATH, self.files)
                    self.sdf = e.clean_file(sdf)
                    self.sindex = self.sdf.index.to_series()
                    self.alldata.senddict[self.ecsocket].put(self.senddataproc("cleandf",self.sindex))
                elif(command is "cleandf"):
                    print("in cleandf block")
                    self.oindex = data
                    self.sdf = self.sdf.join(self.oindex, how ="inner")
                    self.sdf =self.sdf.drop('index', axis=1)
                    if(self.qsource):
                        sxor_2half =e.xor_df(e.split_2half(self.sdf), self.sdf)
                        sxor_oddeven = e.xor_df(e.split_oddeven(self.sdf), self.sdf)
                        self.alldata.senddict[self.ecsocket].put(self.senddataproc("xor_2half", sxor_2half))
                        self.alldata.senddict[self.ecsocket].put(self.senddataproc("xoroddeven", sxor_oddeven))

                                                             
                elif(command is "xor_2half"):
                    self.oxor_2half= data
                    self.sxor_2half =e.xor_df(e.split_2half(self.sdf), self.sdf)
                    self.key_2half = self.oxor_2half[self.oxor_2half['xor']==self.sxor_2half['xor']]
                    ########################################70
                    self.skeylist_2half= self.key_2half.index1.tolist()
                    self.sklist_2half.extend(self.key_2half.index2.tolist())
                    self.keydf_2half =e.df(index=self.sklist_2half)######################79
                    
                    
                elif(command is "xoroddeven"):
                    self.oxor_oddeven = data
                    self.sxor_oddeven = e.xor_df(e.split_oddeven(self.sdf), self.sdf)
                    self.key_oddeven = self.oxor_oddeven[self.oxor_oddeven['xor']==self.sxor_oddeven['xor']]
                    self.skeylist_oddeven= self.key_oddeven.index1.tolist()
                    self.sklist_oddeven.extend(self.key_oddeven.index2.tolist())
                    self.keydf_oddeven =e.df(index=self.sklist_oddeven)############80

                    ############# join the 2 keydf and send the index to the other node
                    self.keydf = self.keydf_2half.join(self.keydf_oddeven, how='inner')
                    print(self.keydf)
                    

                elif(command is "keydf"):
                    pass
            
           
    def senddataproc(self, command, data):
        data = SendData(command, data)
        data = pickle.dumps(data)
        return data
    def receiveddataproc(self, data):
        data =pickle.loads(data)
        return data.command, data.data
    
            
    def off(self):
        self.switch.set()

class SendData():
    '''object to wrap the command and the following data for sending over the network'''
    def __init__(self, command, data):
        self.command = command
        self.data = data
