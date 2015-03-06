import json

__author__ = 'Gerryflap'
import socket
try:
    import _thread
except Exception:
    import thread as _thread
import time

def connect(ip, port):
    mySocket = socket.create_connection((ip, port))
    return Connection(mySocket)



class Connection(object):
    def __init__(self, sock):
        self.sock = sock
        self.ports = {}
        self.port = 0
        _thread.start_new_thread(self.listen, tuple())


    def addConnection(self):
        lastPort = self.port
        print("Sending a port request over socket %s"%(self.sock))
        self.sock.send(bytes(json.dumps({"type": "REQUEST"}), 'UTF-8'))
        print("Sent a port request over socket %s"%(self.sock))
        while self.port == lastPort:
            time.sleep(0.01)
        newPortConnection = PortConnection(self, self.port)
        self.ports[str(self.port)] = newPortConnection
        return (newPortConnection, self.port)

    def listen(self):
        print("Started listening")
        while True:
            recieved = self.sock.recv(4096)
            if(len(recieved) != 0):
                try:
                    recieved = json.loads(recieved.decode("utf-8"))
                    if "type" in recieved:
                        self.handleProtocol(recieved)
                except ValueError:
                    pass

    def handleProtocol(self, data):
        type = data["type"]

        if type == "DATA":
            if data["port"] in self.ports:
                self.ports[data["port"]].onRecv(data)
        elif type == "REQUEST_OK":
            self.port = data["port"]
            print("New port opened on %s"%self.port)

    def closeConnection(self, port):
        del self.ports[port]

    def send(self, data):
        self.sock.send(data)

class PortConnection(object):
    def __init__(self, connection, port):
        self.connection = connection
        self.port = port
        self.listener = 0

    def onRecv(self, data):
        if self.listener != 0:
            try:
                try:
                    self.listener.onRecv(data["data"])
                except ValueError as e:
                    print(e)
            except AttributeError as e:
                print("Error: Please add a onRecv(self, data) method to your object!")
        else:
            print("Recieved %s, but no listener has been added"%data)

    def send(self, port, data):
        self.connection.send(bytes(json.dumps({"type": "DATA", "port": port, "data": data}), 'UTF-8'))

    def setListener(self, object):
        print("Added listener: %s"%object)
        self.listener = object