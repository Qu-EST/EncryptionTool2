'''module contais the serverlogin node widgets'''
from tkinter import Frame, Button, Label, Entry

class ConnectButton(Button):
    '''extension of the Button. Connects to the client.
    part of the Node Frame'''
    def __init__(self, master):
        super.__init__(self, master, text="Connect", command=self.connect, width=12)

    def connect(self):
        '''the connection actions'''
        pass


class DisconnectButton(Button):
    '''extension of the Button. Connects to the client.
    part of the Node Frame'''
    def __init__(self, master):
        super.__init__(self, master, text="Connect", command=self.connect, width=12)

    def disconnect(self):
        '''the connection actions'''
        pass



class MessengerButton(Button):
    '''extension of the Button. Connects to the client.
    part of the Node Frame'''
    def __init__(self, master):
        super.__init__(self, master, text="Connect", command=self.connect, width=12)

    def messenger(self):
        '''the connection actions'''
        pass


class ErrorcheckBurron(Button):
    '''extension of the Button. Connects to the client.
    part of the Node Frame'''
    def __init__(self, master):
        super.__init__(self, master, text="Connect", command=self.connect, width=12)

    def errorcheck(self):
        '''the connection actions'''
        pass

class NodeFrame(Frame):
    '''NodeFrame has the buttons to communicate with the nodes connected'''
    def __init__(self, master):
        self.super.__init__(self, master)
        self.connectbutton = ConnectButton(self)
        self.disconnectbutton =DisconnectButton(self)
        self.messengerbutton = MessengerButton(self)
        self.errorcheckbutton = ErrorcheckBurron(self)
        
        # add the above buttons
        self.connectbutton.pack(side=LEFT)
        self.DisconnectButton.pack(side=LEFT)
        self.messengerbutton.pack(side=LEFT)
        self.errorcheckbutton.pack(side=LEFT)
        
