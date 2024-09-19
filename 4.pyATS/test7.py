# allow testbed to be loaded in
from genie.testbed import load
from rich import print as pprint
import json

testbed = load('testbed.yaml')
device_one = testbed.devices['NewYork']

# minimize log output on screen when running test
device_one.connect(log_stdout=False)

# interface_info = device_one.parse("show cdp neighbors")
# cdp = interface_info['cdp']['index']
# for index in cdp:
#     remote_device = cdp[index]['device_id']
#     local_intf = cdp[index]['local_interface']
#     remote_intf = cdp [index]['port_id']
#     pprint(f"{device_one} is connected to {remote_device} GigabitEthernet{remote_intf} on local interface {local_intf}")

route_info = device_one.parse("show ip route")
parse_route = route_info['vrf']['default']['address_family']['ipv4']['routes']

for routes in parse_route:
    parsed = parse_route[routes]
    route = parsed['route']
    protocol = parsed['source_protocol']
    outer_dict = parsed['next_hop'].items()
    for k,v in outer_dict:
        for intf, intf_details in v.items():
            egress_intf = intf_details.get('outgoing_interface', 'NA')
            pprint(f"{device_one}, Route: {route}, Protocol: {protocol}, Outbound: {egress_intf}")
