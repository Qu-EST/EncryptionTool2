'''
Created on Apr 28, 2017

@author: jee11
'''
from threading import Thread
from queue import Queue
import time
class TestTimeProducer(Thread):
    '''
    classdocs
    '''


    def __init__(self, hash_queue):
        '''
        Constructor
        '''
        Thread.__init__(self)
        self.hash_queue=hash_queue
        
    def run(self):
        while(1):
            self.hash_queue.put("75.66")
            time.sleep(2)