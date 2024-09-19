# allow testbed to be loaded in
from genie.testbed import load
from rich import print as pprint

ospf_count = []
testbed = load('testbed.yaml')

# Dictionary to store OSPF routes for each device
device_routes = {}

# Iterate over each device in the testbed
for device in testbed.devices:
    dev = testbed.devices[device]
    dev.connect(log_stdout=False)
    
    # Parse OSPF routes
    ospf_test = dev.parse("show ip route ospf")['vrf']['default']['address_family']['ipv4']['routes']
    
    # Initialize a list to hold OSPF routes for this device
    ospf_count = []
    
    # Iterate over the routes and collect the source_protocol
    for route in ospf_test:
        protocol = ospf_test[route].get('source_protocol')
        ospf_count.append(protocol)
    
    # Count the number of OSPF routes
    total = ospf_count.count('ospf')
    
    # Store the count in the dictionary
    device_routes[dev.name] = {
        'total': total,
        'routes': ospf_count
    }

# Print the results
for device_name, info in device_routes.items():
    pprint(f"Device: [yellow]{device_name}[/yellow] has {info['total']} [green]OSPF[/green] routes learned.")


