'''
Created on Apr 27, 2017

@author: jee11
'''
from threading import Thread
import datetime
from queue import Queue
import os

class SaveFile(Thread):
    '''
    classdocs
    '''


    def __init__(self, save_data=Queue(0)):
        '''
        Constructor
        '''
        Thread.__init__(self)
        self.save_data=save_data
        self.filename=datetime.date.strftime(datetime.datetime.now(),'%m-%d_%H-%M-%S')+".txt"
        #os.chdir(r'C:\Users\Quest01\Documents\TDCData')
        print(os.getcwd())
        self.datafile=open(self.filename,"a+")
        self.switch=1
        self.setDaemon("True")
        
    def run(self):
        #print("inside run of the save")
        #print(str(~(self.save_data.empty())))
        while(str(self.save_data.empty())=="False"):
            #print("inside while")
            datatowrite=self.save_data.get()
            #print(datatowrite)
            self.datafile.write(datatowrite)
            
            self.datafile.write("\n")
        self.datafile.close()
        
                
                
    def off(self):
        self.switch="False"