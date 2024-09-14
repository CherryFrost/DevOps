from pyats import aetest
from pyats.topology import loader
from genie.testbed import load
from pprint import pprint
from genie.utils import Dq

# Load the Testbed File
tb = loader.load('inventory/testbed.yml')
# Assign the DevNetRouter device to a variable
vIOS = tb.devices['R1-NewYork']
# Connect to the DevNet Router
vIOS.connect()
x = pprint(vIOS.parse('show ip route'))
if 'metric' == 0 in x['vrf']['default']['address_family']['ipv4']['routes']['10.1.1.1/32']:
    print("Yes")
else:
    print("No")
