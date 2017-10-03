'''
Created on Apr 13, 2017

@author: jee11
'''
from threading import Thread, Event
import re
import datetime
from queue import Queue
from QuEST.EncryptorData import EncryptorData
import win32api
from test.test_logging import pywintypes
import time
from queue import LifoQueue
from conda._vendor.auxlib._vendor.five import string
class TDCReaderThread(Thread):
    '''
    classdocs
    '''


    def __init__(self, tdc_reader, hash_queue=Queue(0), interface="tdc"):
        '''
        Constructor
        '''
        Thread.__init__(self)
        self.hash_queue=hash_queue
        self.tdc_reader=tdc_reader
        self.tdc_switch=Event()
        self.tdc_switch.clear()
        self.tdc_reader.start_TDC()
        self.interface=interface
        self.alldata=EncryptorData()
        self.now=datetime.datetime.now()
        self.counter=0
        
    def run(self):
        if(self.interface=="tdc"):
            self.start_reading()
        else:
            print("reading time")
#             self.counter=0
            self.read_time()
        
    def read_time(self):    
        print("reading the GPS time")
        now=self.now
        # filename=datetime.date.strftime(datetime.datetime.now(),'%m-%d_%H-%M-%S')+"timer_log.txt"
        # datafile=open(filename, "a+")


        while(not self.tdc_switch.is_set()):
            byte_data=self.tdc_reader.readline()
            # print(byte_data)
            try:
                self.gpsdata=byte_data.decode('utf-8')
                
            except UnicodeDecodeError as e:
                print("unicode decode error from the gps reader: {}".format(e))
            else:
                gpsdata=self.gpsdata
                if(gpsdata[0:6]=="$GPGGA"):
                    timestamp=gpsdata[7:17]
                    # self.alldata.gpstime=timestamp
                    try:
                        hour=int(gpsdata[7:9])
                        min=int(gpsdata[9:11])
                        sec=int(gpsdata[11:13])
                        mmm=int(gpsdata[14:17])
                        day=now.day
                        month=now.month
                        year=now.year
    #                     time_str=(year+month+day+hour+min+sec+mmm)
                        
                        dayOfWeek = datetime.datetime(year,month, day, hour=hour,minute=min,second=sec, microsecond=mmm).isocalendar()[2]
                    except ValueError as e:
                        print("error while decodng the time from GPS {}".format(e))
                    else:
                        try:    
                            tempstamp="{},{},{},{}".format(hour,min,sec,mmm)
                            # CODE FOR THE GPS TIME WITH CONDITION
                            # with self.alldata.gpstime_condi:
                            #      # print("acquired lock")
                            #      self.alldata.gpstime=tempstamp
                            #      # self.alldata.gpstime_condi.notify()

                            # CODE FOR THE GPS WITH LIFO QUEUE
                            self.alldata.gpsqueue=LifoQueue(0)
                            self.alldata.gpsqueue.put(tempstamp)
                            self.alldata.good_ut.put(tempstamp)
                            # print("lock released")
                            # win32api.SetSystemTime( year,month,dayOfWeek, day, hour, min, sec, mmm )
                            # print("time changed to {}".format(timestamp))

                            # print("updated time: {}".format(self.counter))
                            # self.counter=self.counter+1


                            # datafile.write("time changed to {}".format(timestamp)) 

                            # print("updated time: {}".format(self.counter)) 
                            # self.counter=self.counter+1 
                           
                        except pywintypes.error as e:
                            print("error while setting the time in the system: {}".format(e))
                    #print(timestamp)
            
        print("closing the com port")
        self.tdc_reader.stop_TDC()
        # datafile.close()
        print(self.tdc_reader)    
    def start_reading(self):
        oldgps=0
        while(not self.tdc_switch.is_set()):
            byte_data=self.tdc_reader.readline()
            comp_time=time.perf_counter()
            string_data=byte_data.decode('utf-8')          
            string_data=string_data.rstrip()
            
            try:
                value=int(float(string_data))
            except ValueError as e: 
                print(e) 
                value =0
            if(value>0):
                self.counter=self.counter+1
            else:
                self.counter=0
#            string_data="{},{}".format(time.perf_counter(),string_data)
#             string_data=string_data.zfill(5)
#             macrotime=datetime.date.strftime(datetime.datetime.now(),'%m,%d,%H,%M,%S,%f')
#             data=macrotime+','+string_data[:3]+','+string_data[3:]
            #print("waiting to acquire the gpstime")
            # CODE FOR GPS TIME WITH CONDITION
            # with self.alldata.gpstime_condi:
            #    # self.alldata.gpstime_condi.wait_for(self.tdc_switch.is_set)
            #     print("acquired the gps time")
            #     gpstime=self.alldata.gpstime

            # CODE FOR THE GPS WITH LIFO QUEUE
            if(self.alldata.gpsqueue.empty()):
                gpstime=oldgps
            else:
                gpstime=self.alldata.gpsqueue.get()
                #self.alldata.gpsqueue=LifoQueue(0)
                oldgps=gpstime
            #try:    
#             data=str(gpstime)+","+str(string_data[:3])+","+str(string_data[3:])
            data="{},{},{},{}".format(self.counter, gpstime, comp_time, string_data)
           # except TypeError as e: print(e) print(type)
            #print(data)
            self.hash_queue.put(data)
            #self.hash_queue.task_done()
        print("closing the com port")
        self.tdc_reader.stop_TDC()
        print(self.tdc_reader)
        #print("clearing the hash queue")
        #self.hash_queue=Queue()
                        
    def off(self):
        print("inside tdc reader off")
        self.tdc_switch.set()
        #print(self.tdc_reader)        
