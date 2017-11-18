'''encryptorui'''

from tkinter import Tk, TOP, RIGHT, LEFT, Radiobutton, W, IntVar
import threading
from UI.uart_widgets import SettingsFrame
from UI.com_widgets import IP_Communication_settings
from UI.scom_widgets import *
class EncryptionUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Encryption Tool")
        self.setting_frame = SettingsFrame(self)
        self.setting_frame.pack(side=LEFT)
        self.commframe=CommFrame(self)
        self.commframe.pack(side=RIGHT)
        self.protocol("WM_DELETE_WINDOW", self.on_exit())
        


    def on_exit(self):
        print("on exit")
        
#         
        print("closing the threads")
        for threads in threading.enumerate():
            if(not((threads.name=='MainThread') or threads.isDaemon())):
                
                #if(threads.)
                print("closing the thread "+threads.name)
                print(threads)
                try:
                    threads.off()
                    print(type(threads))
                    print(threads.is_alive())
                    threads.join()
                except AttributeError as e:
                    print("the thread: {} does not have off. hence skipping to close it.".format(threads.name))
                
                        
        print(threading.active_count())
        try:
            self.all_data.encrypt_socket.close()
        except AttributeError:
            print("no socket to close")
        self.quit()
#         time.sleep(2)
        print(threading.enumerate())
        self.quit()

class CommFrame(Frame):
    def __init__(self, master):
        self.master=master
        Frame.__init__(self, master)
        self.console =None
        self.ip_comm_frame= IP_Communication_settings(self) 
        # self.ip_comm_frame.pack(side=RIGHT)
        self.sercomframe= ServerComFrame(self)
        # self.sercomframe.pack(side=RIGHT)

       
        self.v=IntVar()
        self.ipset = Radiobutton(self, text="ip Setting", variable=self.v, value =1, command=self.displaysetting).pack(anchor=W)
        self.serverset = Radiobutton(self, text = "server login", variable =self.v, value=2, command=self.displaysetting).pack(anchor=W)


    def displaysetting(self):
        if(self.v.get()==1):
            self.sercomframe.node1.pack_forget()
            self.ip_comm_frame.pack(side=RIGHT)
        elif(self.v.get()==2):
            self.sercomframe.node1.pack(side=RIGHT)
            self.ip_comm_frame.pack_forget()
            
        
