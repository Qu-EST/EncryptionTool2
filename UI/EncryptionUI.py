'''encryptorui'''

from tkinter import Tk, TOP, RIGHT, LEFT
import threading
from UI.uart_widgets import SettingsFrame
from UI.com_widgets import IP_Communication_settings
class EncryptionUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.setting_frame = SettingsFrame(self)
        self.setting_frame.pack(side=LEFT)
        self.ip_comm_frame= IP_Communication_settings(self)
        self.ip_comm_frame.pack(side=RIGHT)
        

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
