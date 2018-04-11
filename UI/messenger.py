'''
Created on dec 22, 2017

'''
from tkinter import Tk, Text, Frame, Entry, Button, Label, Toplevel
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
import socket
import pickle
from COMM import tools
from distutils.command.check import check
from PIL import ImageTk, Image
import datetime
class popup(object):
    def __init__(self, master, action="close"):
        self.master=master
        self.action=action
        self.master.attributes("-topmost", 0)
        top=self.top=Toplevel(master)
        top.attributes("-topmost", 1)
        top.attributes("-fullscreen", 1)
        top.protocol("WM_DELETE_WINDOW", self.enable_top)
        self.wrong_pass =Label(top, text="wrong password")
        self.pass_label = Label(top, text="Password")
        self.pass_entry = Entry(top, show="*")
        self.submit_button = Button(top, text="Submit", command=self.submit)
        self.close_button =Button(top, text ="Cancel", command=self.enable_top)
        self.pass_label.grid(column=0, row=1)
        self.pass_entry.grid(column=1, row=1)
        self.submit_button.grid(column=1, row=2)
        self.close_button.grid(column=2, row=2)
    
    def enable_top(self):
        self.master.attributes("-topmost", 1)
        self.top.destroy()
        
    def submit(self):
        password = self.pass_entry.get()
        print(self.action)
        if(password=="lpj"):
            self.top.destroy()
            if(self.action=="close"):
                self.alldata=EncryptorData()
                self.alldata.messenger=""
                self.master.destroy()
            elif(self.action=="min"):
                self.master.wm_state("iconic") 
        else:
            self.wrong_pass.grid(column=0, row=0)
            
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
        self.attributes("-topmost",1)
        self.attributes("-fullscreen", 1)
        self.messenger_frame=Frame(self)
        self.messenger_frame.pack()
        if(type(messenger_socket)!= socket.socket):
            ip = messenger_socket
            messenger_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            messenger_socket.connect((ip, alldata.MESSENGERPORT))
            messenger_socket.setblocking(0)
            alldata.inputs.extend([messenger_socket])
            tools.messenger_init(messenger_socket)
        self.send_queue=alldata.send_data
        self.title_label=Label(self.messenger_frame,text="Quantum Messenger",font=("Helvetica", 16))
        self.title_label.grid(row=0,column=0,columnspan=2)
        self.messagepad=Text(self.messenger_frame, height=25, width=160)
        #self.messagepad.config(state=DISABLED)
        self.messagepad.grid(row=1, column=0, columnspan=2)
        self.displaymessage=alldata.displaymessage[messenger_socket]
        self.sent_console = ConsoleFrame(self.messenger_frame, alldata.sent_raw_message[messenger_socket],"Sent Encrypted Message")#)
        self.received_console = ConsoleFrame(self.messenger_frame,  alldata.received_raw_message[messenger_socket], "Received Encrypted Message")#)
        # sent and received consoles initlizationa and display
        self.sent_console.grid(row=2, column=0, sticky =W)
        self.received_console.grid(row=2, column=1, sticky =W)
        self.sendframe=SendFrame(self.messenger_frame,self.send_queue,self.displaymessage,alldata, messenger_socket)
        self.sendframe.grid(row=3, column=0, columnspan =2, sticky =W)
        self.window_opt_frame=Frame(self.messenger_frame)
        self.window_opt_frame.grid(row=5, column=0, columnspan=2)
        self.close_button = Button(self.window_opt_frame, text="close", command=self.on_exit)
        self.close_button.grid(row=0, column=0)
        self.minmize_button = Button(self.window_opt_frame, text="minimize", command=self.on_min)
        self.minmize_button.grid(row=0, column=1)
        self.display=DisplayThread(self.messagepad,self.displaymessage)
        self.display.start()
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.alldata=alldata
        self.welcome_label=Label(self.messenger_frame, font=("Helvetica", 16), text="Welcome to Quantum Corner. \nYou are sending messages to another quantum node in Burchard 616 \nThese messages are encrypted by entangled photons states. \nWhat do you think?")
        self.welcome_label.grid(row=4, column=0, columnspan=2)
        #self.sendframe.bind("<Return>", lambda x: self.sendframe.send())
        #C:\\Users\\jee11\\OneDrive\\Documents\\QuEST\\EncryptionTool2\\poster
#         image=Image.open("Slide7.jpg")
#         print(image)
#         poster_frame=(self)
#         poster_frame.pack()
#         poster = PhotoImage(image, master=poster_frame)
#         print(poster)
#         poster_label =  Label(poster_frame, image=poster)
#         poster_label.pack()
#     
    def on_exit(self):
        check_quit = popup(self)
        self.wait_window(check_quit.top)
    def on_min(self):
        check_min = popup(self, action="min")
        self.wait_window(check_min.top)
    def setkey(self):
        self.sendframe.setkeylabel()    
        
        
        
    
        
        
class SendFrame(Frame):
    
    def __init__(self,master,send_queue,messagequeue,alldata, messenger_socket):
        Frame.__init__(self,master)
        self.messenger_socket = messenger_socket
        self.alldata=alldata
        self.send_queue=send_queue
        self.messagequeue=messagequeue
        self.entry=Entry(self,width=150)
        self.sendbutton=Button(self,command=self.send,text="Send", width=12)
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
            #self.send_queue.put("message "+to_send)
            self.alldata.senddict[self.messenger_socket].put("message "+to_send)
            self.alldata.sent_raw_message[self.messenger_socket].put("message "+to_send)
            self.alldata.outputs.append(self.messenger_socket)
        else:
            try:
                encrypted_data=self.alldata.encryptor.encode(to_send,tfh)
            except LookupError:
                self.alldata.encryptor=Encryptor(b'7774')
                encrypted_data=self.alldata.encryptor.encode(to_send, tfh)
                
            msg_data = tools.message_obj(index, encrypted_data, None)
            self.alldata.senddict[self.messenger_socket].put(pickle.dumps(msg_data))
            self.alldata.sent_raw_message[self.messenger_socket].put(str(index).encode() + b' ' + encrypted_data)
            self.alldata.outputs.append(self.messenger_socket)
        
        self.messagequeue.put(datetime.date.strftime(datetime.datetime.now(),'%m/%d-%H:%M:%S')+"\nME: "+to_send)
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
                    
            self.key_label.config(text="Message to send")
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
                
