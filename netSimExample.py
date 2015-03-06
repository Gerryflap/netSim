__author__ = 'Gerryflap'
import netSimClient as nsc

#Connect to the server running the simulation
connection = nsc.connect("127.0.0.1", 1337)


#Define a class that will be connected to the virtual network
class Computer(object):
    def __init__(self):
        print("Init")

        #Connect with the virtual router, this gives us our potrnumber and a portConnection, used for communication
        (self.portConnection, self.port) = connection.addConnection()
        print("Connected to virtual port %s"%(self.port))
        self.portConnection.setListener(self)

        #Send a dictionary via our PortConnection
        #Whatever is in the dictionary is up to you.
        print("Sending text")
        self.portConnection.send(0, {"text": "Zwekker"})
        print(self.port)

    def onRecv(self, data):
        #Define a function to handle recieved data. This method needs to exist!
        print(data)

    def stuurBericht(self):
        #A custom method used to send messages to certain other connected devices.
        poort = input("Poort: ")
        bericht = input("Bericht: ")
        self.portConnection.send(poort, bericht)


computer = Computer()

#The main thread should be kept alive, otherwise the program will finish and disconnect.
while True:
    computer.stuurBericht()