__author__ = 'Gerryflap'
import netSimClient as nsc
import time

class netSimRouter(object):

    def __init__(self, connection, ip = 0, subnetsize = 0):
        self.connectedDevices = {}
        self.ipList = {}
        self.ip = ip
        self.subnetsize = subnetsize
        self.ipCounter = 0
        self.portCounter = 0
        (self.portConnection, self.port) = connection.addConnection()
        self.portConnection.setListener(self)
        self.connect(self.portConnection)
        self.unicast("0", {"type": "DHCP_REQUEST"})



    def connect(self, device):
        self.connectedDevices[str(self.portCounter)] = device
        self.portCounter += 1

    def onRecv(self, data):
        if "toIp" in data:
            toPort = self.lookup(data["tooIp"])
            if  toPort != "-1":
                self.unicast(toPort, data)
            else:
                if "fromPort" in data:
                    self.broadcast(data["fromPort"], data)
                else:
                    self.broadcast(0, data)

        if "fromIp" in data and "fromPort" in data:
            self.store(data["fromIp"], data["fromPort"])

        if "type" in data and data["type"] == "DHCP_REQUEST" and "fromPort" in data and self.subnetsize != 0:
            self.unicast(data["fromPort"], {"type": "DHCP_RESPONSE", "ip": self.ipCounter, "subnetSize": min(self.subnetsize - 8, 0)})
            self.ipCounter += + 2**self.subnetsize

        if "type" in data and data["type"] == "DHCP_RESPONSE":
            self.ip = int(data["ip"])
            self.subnetsize = int(data["subnetSize"])
            self.ipCounter = self.ip + 2**self.subnetsize


    def unicast(self, port, data):
        if port == "0":
            self.portConnection.send("-1", data)
        else:
            if port in self.connectedDevices:
                self.connectedDevices[port].recv(data)

    def broadcast(self, fromPort, data):
        for port in self.connectedDevices.keys():
            if port != fromPort:
                self.unicast(port, data)

    def store(self, ip, port):
        self.ipList[ip] = [port, time.time() + 50000]

    def lookup(self, ip):
        if ip in self.ipList:
            return self.ipList[ip]
        else:
            return "-1"

    def send(self, data, fromPort = "-1"):
        if fromPort != "-1":
            data["fromPort"] = fromPort
        self.onRecv(data)

    def step(self):
        currentTime = time.time()
        for ip, ipInfo in self.ipList.items():
            if ipInfo[1] < currentTime:
                del self.ipList[ip]

