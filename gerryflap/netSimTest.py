__author__ = 'Gerryflap'
import netSimClient as nsc
import gerryflap.netSimRouter as nsr

connection = nsc.connect("www.gerben-meijer.nl", 1337)

router = nsr.netSimRouter(connection)

while True:
    router.step()
