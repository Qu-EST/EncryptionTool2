'''module for the errorcheking thread'''
from queue import Queue, Empty
import EncryptorData
from threading import Thread,Event
from COMM import ErrorChecking as e
import pickle


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
        print("Ec thread")
        if self.qsource:
            if not self.alldata.filelist:
                self.files = self.alldata.files

                #################################
                self.files = "08-24_16-26-38 CW 1mW bur.csv"
            else:
                self.files = self.alldata.filelist[-1]
            print("sending the filename")
            data = self.senddataproc("filename", self.files)
            self.alldata.senddict[self.ecsocket] = Queue(0)
            self.alldata.senddict[self.ecsocket].put(data)
            self.alldata.outputs.append(self.ecsocket)
            print("the items in the outputs {}".format(self.alldata.outputs))
            print("the items in the inputs {}".format(self.alldata.inputs))
        while not self.switch.is_set():
            try:
                receiveddata = self.alldata.receiveddict[self.ecsocket].get(timeout=1)
            except Empty:
                pass
            else:
                command, data = self.receiveddataproc(receiveddata)
                print(command)
                if(command == "filename"):
                    print("in file name block")
                    PATH = "C:\\Users\\jee11\\OneDrive\\Documents\\QuEST\\EncryptionTool2"
                    self.files = "08-24_17-26-36 CW-1mW bab.csv"
                    self.sdf = e.read_file_gps_coun(PATH, self.files)
                    self.sdf = e.clean_file(self.sdf)
                    self.sindex = self.sdf.index.to_series()
                    self.alldata.senddict[self.ecsocket].put(self.senddataproc("cleandf",self.sindex))
                    self.alldata.outputs.append(self.ecsocket)
                   
                elif(command == "cleandf"):
                    print("in cleandf block")
                    self.oindex = data
                    PATH = "C:\\Users\\Quest02\\Documents\\EncryptionTool2"
                    self.sdf = e.read_file_gps_coun(PATH, self.files)
                    self.sdf = e.clean_file(self.sdf)              
                    self.sdf = self.sdf.join(self.oindex, how ="inner")
                    self.sdf =self.sdf.drop('index', axis=1)
                    if(self.qsource):
                        sxor_2half =e.xor_df(e.split_2half(self.sdf), self.sdf)
                        sxor_oddeven = e.xor_df(e.split_oddeven(self.sdf), self.sdf)
                        self.alldata.senddict[self.ecsocket].put(self.senddataproc("xor_2half", sxor_2half))
                        
                        self.alldata.senddict[self.ecsocket].put(self.senddataproc("xoroddeven", sxor_oddeven))
                        self.alldata.outputs.extend([self.ecsocket])
                        self.alldata.outputs.extend([self.ecsocket])
                                                             
                elif(command == "xor_2half"):
                    self.oxor_2half= data
                    self.sxor_2half =e.xor_df(e.split_2half(self.sdf), self.sdf)
                    self.key_2half = self.oxor_2half[self.oxor_2half['xor']==self.sxor_2half['xor']]
                    ########################################70
                    self.skeylist_2half= self.key_2half.index1.tolist()
                    self.sklist_2half.extend(self.key_2half.index2.tolist())
                    self.keydf_2half =e.df(index=self.sklist_2half)######################79
                    
                    
                elif(command == "xoroddeven"):
                    self.oxor_oddeven = data
                    self.sxor_oddeven = e.xor_df(e.split_oddeven(self.sdf), self.sdf)
                    self.key_oddeven = self.oxor_oddeven[self.oxor_oddeven['xor']==self.sxor_oddeven['xor']]
                    self.skeylist_oddeven= self.key_oddeven.index1.tolist()
                    self.sklist_oddeven.extend(self.key_oddeven.index2.tolist())
                    self.keydf_oddeven =e.df(index=self.sklist_oddeven)############80

                    ############# join the 2 keydf and send the index to the other node
                    self.keydf = self.keydf_2half.join(self.keydf_oddeven, how='inner')
                    print(self.keydf)
                    

                elif(command == "keydf"):
                    print("got keydf")
                    print(data)
            
           
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
