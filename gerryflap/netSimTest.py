__author__ = 'Gerryflap'
import netSimClient as nsc
import gerryflap.netSimRouter as nsr

connection = nsc.connect("127.0.0.1", 1337)

router = nsr.netSimRouter(connection)

while True:
    router.step()
