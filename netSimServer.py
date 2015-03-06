__author__ = 'Gerryflap'
import socket
try:
    import _thread
except Exception:
    import thread as _thread
import json

def listenForData(connection):
    global ports
    while True:
        recieved = connection.sock.recv(4096)
        if len(recieved) != 0:
            recievedStr = recieved
            try:
                recieved = json.loads(recieved.decode("utf-8"))
                print(str(recieved))
                if "type" in recieved:

                    type = recieved['type']
                    if(type == "DATA"):
                        if "type" in recieved["data"]:
                            if recieved["data"]["type"] == "DHCP_REQUEST":
                                for aconnection in ports.values():
                                    if aconnection != connection:
                                        aconnection.send(recievedStr)
                        port = recieved["port"]
                        try:
                            print (ports)
                            if port != "-1":
                                ports[port].send(recievedStr)
                            else:
                                for aconnection in ports.values():
                                    if aconnection != connection:
                                       aconnection.send(recievedStr)
                        except KeyError:
                            print("Error: packet sent to non-existing port %s"%port)
                    elif(type == "REQUEST"):
                        print("Port request recieved")
                        connection.addPort()


            except TypeError as e:
                print(e)

class Connection(object):
    def __init__(self, sock):
        self.sock = sock

    def send(self, data):
        print("Sending %s"%data)
        try:
            self.sock.send(data)
        except Exception as e:
            print("Exception while sending: %s"%e)

    def addPort(self):
        global ports
        global portCounter
        ports[str(portCounter)] = self
        self.send(bytes(json.dumps({"type": "REQUEST_OK", "port": portCounter}), "UTF-8"))
        portCounter += 1



port = 1337

ports = {}
portCounter = 1
serverSock = socket.socket()
serverSock.bind(("", port))
serverSock.listen(3)
while True:
    (sock, (ip, portnum)) = serverSock.accept()
    print("A client has connected via %s."%(ip))
    connection = Connection(sock)
    print("New connection object created.")
    _thread.start_new_thread(listenForData, tuple([connection]))#, (connection))
    print("A new listening thread has been started.")
