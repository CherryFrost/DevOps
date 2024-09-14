from pyats import aetest
from pyats.topology import loader
from genie.testbed import load
from pprint import pprint
from genie.utils import Dq

# Load the Testbed File
tb = loader.load('inventory/testbed.yml')
# Assign the R1-NewYork device to a variable
vIOS = tb.devices['R1-NewYork']
# Connect to the NewYork Router
vIOS.connect()

vIOS.configure('''
    interface loopback 1000
    description This was configured using pyATS
    ip address 100.100.100.200 255.255.255.255
    no shut
    ''')
vIOS.execute("sho run interface loopback 1000")
