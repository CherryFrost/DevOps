# allow testbed to be loaded in
from genie.testbed import load
from rich import print as pprint
import json

testbed = load('testbed.yaml')
device_one = testbed.devices['NewYork']

# minimize log output on screen when running test
device_one.connect(log_stdout=False)

interface_info = device_one.learn("interface")

with open('interface_info.json', 'w') as f:
    json.dump(interface_info.to_dict(),f)

with open('interface_info.json', 'r') as r:
     interface_info = json.load(r)
#pprint(interface_info)
for interface, details in interface_info['info'].items():
    mac_addr = details.get('mac_address', 'NA')
    pprint(f"Interface: {interface} has MAC: {mac_addr}")

#pprint(f"[yellow]Device:[/yellow] {hostname} [purple]has a management IP of:[/purple] [yellow]{mgmt_ipAddr}[/yellow]")
