'''widgets related to the uart setting will be defined here
date: 10/03/2017
'''

from tkinter import Frame, IntVar
from tkinter import Label
from tkinter import Entry
from tkinter import *
from threading import Thread, Event
import os, threading
from EncryptorData import EncryptorData

class InputFrame(Frame):
    ''' Frame for the input of the port no. and baud rate'''
    def __init__(self,master,label_text="label"):
        Frame.__init__(self, master,width=350,height=70)
        self.label_text=label_text
        self.label=Label(self,text=label_text,width=12)
        self.entry=Entry(self,width=10)
        self.label.pack(side=LEFT)
        self.entry.pack(side=RIGHT)
    def get_data(self):         
        data=self.entry.get()
        if (data==''):
            if(self.label_text=="Port No"):
                data="COM5"
                return data
            elif (self.label_text=="Baud rate"):
                data=115200
                return data
        else: return data

class SaveButton(Button):
    def __init__(self,master):
        Button.__init__(self,master,text="Save",command=self.start_save,width=12)
        alldata=EncryptorData()
        self.save_data=alldata.save_data
        self.config(state=DISABLED)
    def start_save(self):
        pass
        print("Starting to save")
        self.config(state=DISABLED)
        self.saver=SaveFile(self.save_data)
        self.saver.start()
        
class ChangeButton(Button):        
    def __init__(self,master,console):
        Button.__init__(self,master,text="Load key",command=self.loadkey,width=12)
        self.all_data=EncryptorData()
        all_data=self.all_data
        self.tdc_reader=all_data.tdc_reader
        self.console=console
        self.hash_queue=all_data.hash_queue
        
    def loadkey(self):    
        pass
        os.chdir(r'C:\Users\Quest01\Desktop\EncryptionTool\QuestProject\QuEST')
        keyfile=open("Quantum_Keys.txt",'r')
        keylist=keyfile.readlines()
        index=1
        for keys in keylist:
            #print(keys.rstrip('\n'))
            tempkey={index:keys.rstrip('\n')}
            self.all_data.key.update(tempkey)
            index=index+1
        print(self.all_data.key)
class StartButton(Button):        
    def __init__(self, master, console, interface="tdc"):
        
        self.all_data=EncryptorData()
        all_data=self.all_data
        self.ui=master
        self.console=console            
        self.serial_reader=None
        if(interface=="tdc"):
            Button.__init__(self, master, text="Start", command=self.start, width=12)      
            self.hash_queue=all_data.hash_queue
            self.tdc_reader=all_data.tdc_reader
            
        else:
            Button.__init__(self, master, text="Start", command=self.startgps, width=12)
            self.gps_reader=all_data.gps_reader
        
    def start(self):
        print("Starting to read from TDC")
        
#         if(self.serial_reader is None):
        print("initializing TDC")
        self.serial_reader=TDCReader() #initialize the serial reader
        port=self.ui.port_input.get_data()
        print("from start button. port:{}".format(port))
        self.serial_reader.port=port #set the port number
        self.serial_reader.baudrate=self.ui.baud_input.get_data() #set the baudrate
        if(self.all_data.tdc_reader==""):
            self.tdc_reader=TDCReaderThread(self.serial_reader,hash_queue = self.hash_queue) #initalize the reader thread
            self.tdc_reader.start() #start the thread
            self.all_data.tdc_reader=self.tdc_reader
            self.hasher=KeyHasher()
            self.hasher.start()
            self.all_data.hasher=self.hasher
            #print("from start printing the type of tdc reader " + str(type(self.tdc_reader)))
            #print(type(self.all_data.tdc_reader))
            try:
                if not (self.all_data.mt_console.is_alive()):
                    self.start_console()
            except AttributeError:
                self.start_console()
        self.ui.stop_button.config(state=NORMAL)
        self.config(state=DISABLED)
    def start_console(self):
        print("no console present")
        self.display_ut=TextPadWriter(self.console.micro_time, self.all_data.ut) #initialize the thread to put the data in the textpad
        self.displaygoodut=TextPadWriter(self.console.good_utime, self.all_data.good_ut)
        self.display_ut.start() #start putting the data in the textpad
        self.all_data.mt_console=self.display_ut
        self.displaygoodut.start()
        self.all_data.goodt_console=self.displaygoodut
#         print(threading.active_count())
#         print(threading.enumerate())
            
    def startgps(self):
        print("Starting the GPS timer")
        
        
        if(self.serial_reader is None):
            self.serial_reader=TDCReader() #initialize the serial reader
            port=self.ui.gport_input.get_data()
            #print(port)
            self.serial_reader.port=port #set the port number
            baud=self.ui.gbaud_input.get_data()
            self.serial_reader.baudrate=baud
        if(self.all_data.gps_reader==""):
            self.gps_reader=TDCReaderThread(self.serial_reader, interface="gps") #initalize the reader thread
            self.gps_reader.start() #start the thread
            self.all_data.gps_reader=self.gps_reader
        try:
            if not (self.all_data.mt_console.is_alive()):
                self.start_console()
        except AttributeError:
            self.start_console()
        self.ui.gstop_button.config(state=NORMAL)
        self.config(state=DISABLED)       
class StopButton(Button):        
    def __init__(self,master, interface="tdc"):
        if(interface=="tdc"):
            Button.__init__(self,master,text="Stop",command=self.stop,width=12)
            self.start_button=master.start_button
            self.saver=master.saver            
        else:
            Button.__init__(self,master,text="Stop",command=self.stopgps,width=12)
            self.start_button=master.gstart_button
            
        self.alldata=EncryptorData()        
        self.config(state=DISABLED)
        
    def stop(self):
        pass
        print("Stopping to read from TDC")
        
        print("inside stop button")
        self.tdc_reader=self.alldata.tdc_reader
        hasher=self.alldata.hasher
        mt_console=self.alldata.mt_console
        goodt_console=self.alldata.goodt_console
        try: 
            if(self.tdc_reader.is_alive()):
                self.tdc_reader.off()
                self.tdc_reader.join()
                self.alldata.tdc_reader=""
        except AttributeError:
            print("from the stop. the type of serial reader is not thread{}".format(type(self.serial_reader)))            
        try: 
            if(hasher.is_alive()):
                hasher.off()
                hasher.join()
                self.alldata.hasher=None
        except AttributeError:
            print("from the stop. the type of hasher is not thread{}".format(type(hasher)))
        try:
            if(mt_console.is_alive()):
                self.mt_console.off()
                self.goodt_console.off()
                self.mt_console.join()
                self.goodt_console.join()
        except AttributeError:
            print("from stop. the console has no attributes")
#         self.saver.config(state=NORMAL)
        self.config(state=DISABLED)
        self.start_button.config(state=NORMAL)    
            

    def stopgps(self):
        
        self.start_button.config(state=NORMAL)
        print("inside gps stop button")
        self.tdc_reader=self.alldata.gps_reader
        try: 
            if(self.tdc_reader.is_alive()):
                self.tdc_reader.off()
                self.tdc_reader.join()
                self.alldata.gps_reader=""
        except AttributeError:
            print("from the gps stop. the type of serial reader is not thread{}".format(type(self.tdc_reader)))            
        self.config(state=DISABLED)    
class SettingsFrame(Frame):
    def __init__(self,master):
        Frame.__init__(self, master)
        self.all_data=EncryptorData()
        #TDC Settings
        master.console = None
        self.TDC_part=Label(self,text="TDC Setting",width=25)
        self.port_input=InputFrame(self,label_text="Port No")
        print("port_type")
        print(type(self.port_input))
        self.baud_input=InputFrame(self,label_text="Baud rate")
        self.change_button=ChangeButton(self,master.console)
        self.start_button=StartButton(self,master.console)
        self.saver=SaveButton(self)
        self.stop_button=StopButton(self)
        
        
        self.TDC_part.grid(row=0, column=0, sticky=W)
        self.port_input.grid(row=1,column=0, sticky=W)
        self.baud_input.grid(row=2,column=0,sticky=W)
        self.baud_input.entry.config(state=DISABLED)   #Disabling the baud input temporarily
        self.change_button.grid(row=3,column=0,sticky=W)
        self.start_button.grid(row=4,column=0,sticky=W)
        self.stop_button.grid(row=5,column=0,sticky=W)
        self.saver.grid(row=6,column=0,sticky=W)
        self.saver.config(state=DISABLED)
        
        #GPS Settings
        
        self.GPS_part=Label(self,text="GPS Setting",width=25)
        self.gport_input=InputFrame(self,label_text="Port No")
        print("port_type")
        print(type(self.port_input))
        self.gbaud_input=InputFrame(self,label_text="Baud rate")
        self.gchange_button=ChangeButton(self,master.console)
        self.gstart_button=StartButton(self,master.console,interface="gps")
#         self.gstart_button.config(state=DISABLED)
        #self.saver=UIWidgets.SaveButton(self)
        self.gstop_button=StopButton(self,interface="gps")
        
        
        self.GPS_part.grid(row=0, column=1, sticky=W)
        self.gport_input.grid(row=1,column=1, sticky=W)
        self.gbaud_input.grid(row=2,column=1,sticky=W)
        #self.gbaud_input.entry.config(state=DISABLED)   #Disabling the baud input temporarily
        #self.change_button.grid(row=3,column=1,sticky=W)
        self.gstart_button.grid(row=4,column=1,sticky=W)
        self.gstop_button.grid(row=5,column=1,sticky=W)
