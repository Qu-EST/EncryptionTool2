import pyaes
import math
from twofish import Twofish

class Encryptor(object):
    '''
    classdocs
    '''


    def __init__(self, key):
        '''
        Constructor
        '''
        #self.key=key
        #self.encoder=pyaes.AESModeOfOperationCTR(self.key)
        #self.decoder=pyaes.AESModeOfOperationCTR(self.key)
        #self.tfh=Twofish(key)
        
    def encode(self,message, tfh):
        self.tfh=tfh
        times=math.ceil(len(message)/16)
        counter=1
        enc=b''
        while(times>0):
            times=times-1        
            block=message[((counter-1)*16):(counter*16)]
            #print(len(block))
            #print(block)
            
            try:
                if(counter==1):
                    enc = self.tfh.encrypt(block.encode())
                    #print(enc)
                else:    
                    enc=enc + b' ' + self.tfh.encrypt(block.encode())
                    #print(enc)
            except ValueError:
                block=block.ljust(16)
                enc=enc + b' ' + self.tfh.encrypt(block.encode()) 
                #print(enc)      
            counter=counter+1
        return enc
    
    def decod(self,bytedata, tfh):
        '''code for the aes not used
        '''
        self.tfh=tfh
        try:
            print("inside decoder")
            print(bytedata)
            data= self.decoder.decrypt(bytedata)
            print(data)
            return data
        except:
            pass
        finally:
            return ""
    def decode(self, bytedata, tfh):
        self.tfh=tfh
        print(bytedata)
        message=b''
        splitted=bytedata.split(b' ')
        print("printingn the number of space in the bytedata")
        print(bytedata.count(b' '))
        
        for blocks in splitted:
            print("block")
            print(blocks)
            try:
                message = message + self.tfh.decrypt(blocks)
            except ValueError:
                print("ignored the below text because of error")
                print(blocks)
            
        return message
