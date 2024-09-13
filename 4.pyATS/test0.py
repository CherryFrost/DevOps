from pyats import aetest
from genie.testbed import load
from pprint import pprint
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class HelloWorldSetup(aetest.CommonSetup):
    @aetest.subsection
    def setup1(self, testbed):
        testbed.connect()
        logger.info("Hello World from Setup")

class HelloWorldTest(aetest.Testcase):
    @aetest.test
    def test1(self, testbed):
        arp = testbed.devices['DevNet-Rtr'].parse("sho ip arp")
        assert "192.168.60.150" in arp['interfaces']['GigabitEthernet0/0']['ipv4']['neighbors']

    @aetest.test
    def test2(self, testbed):
        arp = testbed.devices['DevNet-Rtr'].parse("sho ip route")
        assert "10.1.1.1/32" in arp['vrf']['default']['address_family']['ipv4']['routes']
#        assert "192.168.60.150" in arp['interfaces']['GigabitEthernet0/0']['ipv4']['neighbors']

aetest.main(testbed=load('inventory/testbed.yml'))