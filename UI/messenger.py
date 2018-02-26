'''
Created on dec 22, 2017

'''
from tkinter import Tk, Text, Frame, Entry, Button, Label
from tkinter.constants import TOP, LEFT, RIGHT, END, BOTTOM, DISABLED, CENTER, W, NORMAL
#from UI import UIWidgets
from threading import Thread, Lock
from queue import Queue
import time
from COMM.Encryptor import Encryptor
from twofish import Twofish
import random
from UI.consolewidgets import ConsoleFrame
from EncryptorData import EncryptorData
class Messenger(Tk):
    '''
    classdocs
    '''


    def __init__(self, messenger_socket):
        '''
        Constructor
        '''
        Tk.__init__(self)
        alldata = EncryptorData()
        self.title("QuEST Messenger")
        self.send_queue=alldata.send_data
        self.messagepad=Text(self)
        #self.messagepad.config(state=DISABLED)
        self.messagepad.grid(row=0, column=0)
        self.displaymessage=alldata.displaymessage[messenger_socket]
        self.sent_console = ConsoleFrame(self, alldata.sent_raw_message[messenger_socket],"Sent Encrypted Message")#)
        self.received_console = ConsoleFrame(self,  alldata.received_raw_message[messenger_socket], "Received Encrypted Message")#)
        # sent and received consoles initlizationa and display
        self.sent_console.grid(row=0, column=1, sticky =W)
        self.received_console.grid(row=0, column=2, sticky =W)
        self.sendframe=SendFrame(self,self.send_queue,self.displaymessage,alldata)
        self.sendframe.grid(row=0, column=3, sticky =W)
        self.display=DisplayThread(self.messagepad,self.displaymessage)
        #self.display.start()
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.alldata=alldata
        #self.sendframe.bind("<Return>", lambda x: self.sendframe.send())
        
    
    def on_exit(self):
        self.alldata=EncryptorData()
        self.alldata.messenger=""
        #self.alldata.ui.setting_frame.messenger.config(state=NORMAL)
        self.destroy()    
        
    def setkey(self):
        self.sendframe.setkeylabel()    
    
        
        
    
        
        
class SendFrame(Frame):
    
    def __init__(self,master,send_queue,messagequeue,alldata):
        Frame.__init__(self,master)
        self.alldata=alldata
        self.send_queue=send_queue
        self.messagequeue=messagequeue
        self.entry=Entry(self,width=50)
        self.sendbutton=Button(self,command=self.send,text="Send",width=12)
        self.key_label=Label(self)
        self.setkeylabel()
        self.key_label.grid(row=0,column=0,sticky=W)
        self.entry.grid(row=0,column=1,sticky=W)
        self.sendbutton.grid(row=0,column=2,sticky=W)
        self.entry.focus()
        self.entry.bind("<Return>", lambda x: self.send())
        self.alldata.encryptor=Encryptor(b'7774')
    
        
        
    def send(self):
        to_send=self.entry.get()
        print("Sending: "+to_send)
        index=random.randrange(1,100,1)
        key=self.alldata.key[index]
        self.alldata.encrypt_key=key
        self.setkeylabel()
        tfh=Twofish(key.encode())
        if(self.alldata.encrypt_key==""):
            self.send_queue.put("message "+to_send)
        else:
            try:
                encrypted_data=self.alldata.encryptor.encode(to_send,tfh)
            except LookupError:
                self.alldata.encryptor=Encryptor(b'7774')
                encrypted_data=self.alldata.encryptor.encode(to_send, tfh)
            self.send_queue.put((str(index)).encode() + b' ' + encrypted_data)
            
        
        self.messagequeue.put("ME: "+to_send)
        self.entry.delete(0,'end')
        
    def setkeylabel(self):
        if(self.alldata.encrypt_key==""):
            self.key_label.config(text="7774")
            #self.key_label.grid(row=0,column=0,sticky=W)
            #return "no encryption"
        else:
            try:
                text="encryption key: "+self.alldata.encrypt_key.decode('utf-8')
            except AttributeError: 
                text="encryption key: "+self.alldata.encrypt_key
                    
            self.key_label.config(text=text)
            #self.key_label.grid(row=0,column=0,sticky=W)
            #return text
        
        
class DisplayThread(Thread):
    
    def __init__(self,textpad,messagequeue):
        Thread.__init__(self)
        self.messagequeue=messagequeue
        self.textpad=textpad
        self.setDaemon('True')
        
    def run(self):
        self.display()
        
    def display(self):
        while(1):            
            if(~self.messagequeue.empty()):
                data=self.messagequeue.get()
                self.textpad.insert(END,data)
                self.textpad.insert(END,'\n')
                self.textpad.see(END)
                self.messagequeue.task_done()
                time.sleep(1)
                
