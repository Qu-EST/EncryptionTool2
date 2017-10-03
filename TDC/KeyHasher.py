'''
Created on Apr 21, 2017

@author: jee11
'''
from threading import Thread, Event
from queue import Queue, Empty
from QuEST.EncryptorData import EncryptorData
import datetime
class KeyHasher(Thread):
    
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        Thread.__init__(self)
        self.alldata=EncryptorData()
        alldata=self.alldata
        self.goodut=alldata.good_ut
        self.hash_queue=alldata.hash_queue
        self.ut=alldata.ut
        self.send_ut=alldata.good_utsend
        self.hashed_key=alldata.key
        self.save_data=alldata.save_data
        self.counter=0
        self.FORCESTOP=86
        self.alldata=alldata
        self.switch=Event()
        self.switch.set()
        if alldata.filename is None:
            alldata.filename=datetime.date.strftime(datetime.datetime.now(),'%m-%d_%H-%M-%S')+".csv"
        self.filename=alldata.filename
        
        
    def run(self):
        self.hasher()
        
    def hasher(self):
        self.datafile=open(self.filename,"a+")
        while(self.switch.is_set()):
            #print("inside hasher while")
            try:
                #self.key, self.value=self.decompose(self.hash_queue.get())               
                self.value=self.hash_queue.get(timeout=1)
                self.hash_queue.task_done()
            except Empty:
                pass
                # print("no data in the hash queue")
            except ValueError as e:
                print("got error while converting the value{}".format(e))
            
            else:
                #This is commented while upgrading to gps
#                 if(self.value>0):
#                     self.counter=self.counter+1
#                 elif(self.value==0):
#                     self.counter=0
#                     self.alldata.key.clear()
#                     self.alldata.good_utsend=Queue(0)
#                  
#                 
#                 self.data=str(self.counter) +" "+ str(self.value)
                self.ut.put(self.value)
                self.datafile.write(self.value+'\n')
#                 self.datafile.write(r'\n')
#                 self.save_data.put(self.data)
#                 if((self.value>0) and (self.value<self.FORCESTOP)):
#                     self.goodut.put(self.data)
 
        self.datafile.close()
        self.alldata.filename=None
        self.filename=None
        print("exiting the hasher thread")
                    
    def decompose(self,data_string):
        key_value=data_string.partition(" ")
        key=key_value[0]
        string_value=key_value[2].strip(" \r\n")
        value=float(string_value)
        return key, value
    
    def off(self):
        print("inside keyhasher off")
        self.switch.clear()            
        
