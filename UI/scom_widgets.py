'''module contais the serverlogin node widgets'''
from tkinter import Frame, Button, Label, Entry, TOP, LEFT

class ConnectButton(Button):
    '''extension of the Button. Connects to the client.
    part of the Node Frame'''
    def __init__(self, master):
        Button.__init__(self, master, text="Connect", command=self.connect, width=12)

    def connect(self):
        '''the connection actions'''
        pass


class DisconnectButton(Button):
    '''extension of the Button. Connects to the client.
    part of the Node Frame'''
    def __init__(self, master):
        Button.__init__(self, master, text="Disconnect", command=self.disconnect, width=12)

    def disconnect(self):
        '''the connection actions'''
        pass



class MessengerButton(Button):
    '''extension of the Button. Connects to the client.
    part of the Node Frame'''
    def __init__(self, master):
        Button.__init__(self, master, text="Messenger", command=self.messenger, width=12)

    def messenger(self):
        '''the connection actions'''
        pass


class ErrorcheckBurron(Button):
    '''extension of the Button. Connects to the client.
    part of the Node Frame'''
    def __init__(self, master):
        Button.__init__(self, master, text="Error Check", command=self.errorcheck, width=12)

    def errorcheck(self):
        '''the connection actions'''
        pass

class NodeFrame(Frame):
    '''NodeFrame has the buttons to communicate with the nodes connected'''
    def __init__(self, master):
        Frame.__init__(self)
        # buttons
        self.connectbutton = ConnectButton(self)
        self.disconnectbutton =DisconnectButton(self)
        self.messengerbutton = MessengerButton(self)
        self.errorcheckbutton = ErrorcheckBurron(self)
        
        # add the above buttons
        self.connectbutton.pack(side=LEFT)
        self.disconnectbutton.pack(side=LEFT)
        self.messengerbutton.pack(side=LEFT)
        self.errorcheckbutton.pack(side=LEFT)

        #data
        self.ecsocket = None
        self.messengersocket = None
        self.ecthread = None
        self.messenger = None

class ServerComFrame(Frame):
    '''node frames will be added dynamicallyd in there'''
    def __init__(self, master):
        Frame.__init__(self, master)
        self.node1=NodeFrame(self)
        #self.node1.pack(side=TOP)
