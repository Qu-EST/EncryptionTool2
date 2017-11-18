
from tkinter import Frame, IntVar
from tkinter import Label
from tkinter import Entry
from tkinter import *
from threading import Thread, Event
import os, threading
from EncryptorData import EncryptorData
from UI.uart_widgets import *

class CheckBoxFrame(Frame):
    def __init__(self,master,label_text="server"):
        Frame.__init__(self,master,width=350,height=70)
        #self.label=Label(self,text=label_text).pack(side=LEFT)
        self.value=IntVar()
        self.checkbox=Checkbutton(self,text=label_text,variable=self.value)
        self.checkbox.pack()
        
    def getvalue(self):
        return self.value.get()
    
class ConnectButton(Button):        
    def __init__(self,master,console):
        Button.__init__(self,master,text="Connect",command=self.connectthread,width=12)
        self.ui=master
        self.all_data=EncryptorData()
        self.alldata=self.all_data
        self.receiver=self.all_data.receiver
        self.encrypt_socket=self.all_data.encrypt_socket
        self.received_data=self.all_data.received_data
        self.sender=self.all_data.sender
        self.receivedprocessor=self.all_data.receivedprocessor
        self.send_data=self.all_data.send_data
        self.console=console
        self.conT=None
        
    def start_conT(self):    
        print("starting the conneting thread")
        self.conT=threading.Thread(target=self.connect)
        self.conT.setDaemon(True)
        self.conT.start()
        
    def connectthread(self):
        try:
            if self.conT.is_alive():
                print("already connecting. please wait")
            else:
                self.start_conT()
        except AttributeError as E:
            #print("starting the co")
            self.start_conT()
    def connect(self):
        #print("this is wereh the objects of connect belong{}".format(type(self)))
        self.disconnect=self.ui.disconnect
        self.communicate=self.ui.start_sending
        self.messenger_button=self.ui.messenger
        
        print("Connecting to the server/client")
        self.IP=self.ui.IP_input.get_data()
        self.if_server=self.ui.if_server.getvalue()
        if(self.if_server):
            self.con_type="server"
        else:
            self.con_type="client"
        self.encrypt_socket=My_TCP(ip=self.IP,port=5005,con_type=self.con_type).my_socket
        print("connected", self.encrypt_socket)
        self.alldata.encrypt_socket=self.encrypt_socket
        #try:
        self.receiver=Receiver_Thread(display_received=self.alldata.displayreceived, received=self.received_data,rcv_socket=self.encrypt_socket)
#         except ConnectionResetError:
#             print("connection reset. invoking the disconnect button")
#             threading.Thread(target=self.alldata.ui.setting_frame.disconnect.invoke).start()
        self.receiver.start()
        self.alldata.receiver=self.receiver
        self.receivedprocessor=ReceivedProcessor(self.alldata)
        self.receivedprocessor.start()
        self.alldata.receivedprocessor=self.receivedprocessor
        self.sender=Sender_Thread(display_sent=self.alldata.displaysent,tosend=self.send_data,send_socket=self.encrypt_socket)
        self.sender.start()
        self.alldata.sender=self.sender
        try:
            if not (self.all_data.sent_console.is_alive()):
                self.start_console()
        except AttributeError:    
            self.start_console()
            
        self.config(state=DISABLED)
        self.disconnect.config(state=NORMAL)
        #self.communicate.config(state=NORMAL)
        self.messenger_button.config(state=NORMAL)
        threading.Thread(target=self.all_data.ui.setting_frame.change_button.invoke).start()
        
    def start_console(self):
        self.displayersent=TextPadWriter(self.console.sent_data, self.alldata.displaysent)
        self.displayerreceived=TextPadWriter(self.console.received_data, self.alldata.displayreceived)
        self.displayersent.start()
        self.displayerreceived.start()
        self.all_data.sent_console=self.displayersent
        self.all_data.received_console=self.displayerreceived
    
        
class DisconnectButton(Button):        
    def __init__(self,master):
        Button.__init__(self,master,text="Disconnect",command=self.disconnect,width=12)
        all_data=EncryptorData()
        self.alldata=all_data
        self.sockettoclose=all_data.encrypt_socket
        #self.sendprocessor=all_data.sendprocessor
        self.receiver=all_data.receiver
        self.receivedprocessor=all_data.receivedprocessor
        self.sender=all_data.sender
        self.messenger=all_data.messenger
        self.config(state=DISABLED)
        self.master=master
        
        
        # to make all queues empty here
        
        
        #self.send_thread=all_data.
    def disconnect(self):
        print("inside the disconnect")
        self.connect=self.master.connect
        self.communicate=self.master.start_sending
        self.messenger_button=self.master.messenger
        print("disConnecting to the server/client")
        
        try:
            print("Trying to close the Messenger")
            self.alldata.messenger.destroy()
            print("messenger closed")
        except AttributeError:
            pass 
            print("no messenger now to destroy")
        except TclError:
            pass
            print("messenger already closed")
        try:
            self.alldata.sendprocessor.off()
        except AttributeError:
            print("no send processor present")
        #self.alldata.encrypt_socket.settimeout(1)
        print("closing the receiver")
        try:
            self.alldata.receiver.off()
            self.alldata.receiver.join()
            self.alldata.recever=""
            print("receiver closed/n closing the received processor")
            self.alldata.receivedprocessor.off()
            self.alldata.receivedprocessor.join()
            self.alldata.receivedprocessor=""
            print("reciever processor closed/n closig the sender")
            self.alldata.sender.off()
            self.alldata.sender.join()
            self.alldata.sender=""
            print("Sender closed\n closing the socket")
            self.alldata.encrypt_socket.close()
            print("socket closed")
        
        except AttributeError as e:
            print("from disconnect button. No connection to disconnect")        
        self.connect.config(state=NORMAL)
        self.config(state=DISABLED)
        self.communicate.config(state=DISABLED)
        self.messenger_button.config(state=DISABLED)
        #print(threading.enumerate())
        
        
class StartSendingButton(Button):        
    def __init__(self,master):
        Button.__init__(self,master,text="Error Check",command=self.send,width=12)
        alldata=EncryptorData()
        self.alldata=alldata
        self.sendprocessor=alldata.sendprocessor
        self.config(state=DISABLED)
    def send(self):
        pass
        print("Communicating with the other lab")
        self.sendprocessor=SendProcessor(self.alldata)
        self.sendprocessor.start()
        self.alldata.sendprocessor=self.sendprocessor
        
        
class MessengerButton(Button):
    def __init__(self,master):
        Button.__init__(self,master,text="Messenger",command=self.start_messenger,width=12)
        alldata=EncryptorData()
        self.alldata=alldata
        self.messenger=alldata.messenger
        self.config(state=DISABLED)
    def start_messenger(self):
        pass
        print("Starting the messenger")
        self.config(state=DISABLED)
        self.messenger=Messenger(self.alldata)
        self.alldata.messenger=self.messenger
        self.messenger.mainloop()


class IP_Communication_settings(Frame):        
    def __init__(self,master):
        Frame.__init__(self, master)
        self.all_data=EncryptorData()
        #Communication Settings
        self.comm_part=Label(self,text="Communication Setting",width=25)
        self.IP_input=InputFrame(self,label_text="IP:")
        self.if_server=CheckBoxFrame(self,label_text="Server")
        self.connect=ConnectButton(self,master.console)
        self.disconnect=DisconnectButton(self)
        self.start_sending=StartSendingButton(self)
        self.messenger=MessengerButton(self)
        
        self.comm_part.grid(row=0,column=0,sticky=W)
        self.IP_input.grid(row=1,column=0,sticky=W)
        self.if_server.grid(row=2,column=0,sticky=W)
        self.connect.grid(row=3,column=0,sticky=W)
        self.disconnect.grid(row=4,column=0,sticky=W)
        
        self.start_sending.grid(row=5,column=0,sticky=W)
        self.messenger.grid(row=6,column=0,sticky=W)
