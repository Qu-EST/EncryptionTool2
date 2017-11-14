class ConsoleFrame(Frame):
    def __init__(self,master, console_name="micro time"):
        Frame.__init__(self,master)
        self.label=Label(self,text=console_name)
        self.console=Text(self,width=30)
        self.label.pack()
        self.console.pack()
        
class TextPadWriter(Thread):
    def __init__(self, text_pad, data_queue):
        Thread.__init__(self)
        self.data_queue=data_queue
        self.text_pad=text_pad.console        
        self.setDaemon(True)
        self.switch=Event()
        self.switch.set()
        
    def run(self):
        self.display()        
    
    def display(self):
        linecount=lambda T: (int(T.index('end').split('.')[0])-1)
        #if(self.switch.is_set()): print("switch is set: before the while loop")
        while(self.switch.is_set()):
            #print(self.switch.is_set())
            #if(self.switch.is_set()): print("switch is set: inside the while loop")
            #print(linecount(self.text_pad))
            if(linecount(self.text_pad)>40):
#                 print("exceeded 40 lines in console")
                self.text_pad.delete("1.0","10.0")
            try:
                data=self.data_queue.get(timeout=1)
                self.data_queue.task_done()
            except Empty: pass
                #print("no data in queue")    
            else:
                try:
                    self.text_pad.insert(END,(data+ '\n'))
                except:
                    self.text_pad.insert(END,data)
                    self.text_pad.insert(END,'\n')
                finally:
                    pass
                    self.text_pad.see(END)
                
                 
    def off(self):
        print("inside the textpad writer off")
        self.switch.clear()
        self.switch.clear()
        print(self.switch.is_set())
        print("starting the wait to check if the switch is set to true")
        self.switch.wait()
        print("exited wait")            
                         
