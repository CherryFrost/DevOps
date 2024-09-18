# allow testbed to be loaded in
from genie.testbed import load
from rich import print as pprint

testbed = load('testbed.yaml')

for device in testbed.devices:
    dev = testbed.devices[device]
    dev.connect(log_stdout=False)
    ntp_servers = dev.parse("show ntp associations")["peer"]
    for ntp_server in ntp_servers:
        assert ntp_server == "1.1.1.1"
        print(f"Test passed: {dev} has an ntp server of {ntp_server}")
