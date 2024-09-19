# Import necessary modules
from genie.testbed import load
from rich import print as pprint

# Load the testbed file
testbed = load('testbed.yaml')

# Dictionary mapping each device to its expected router ID
expected_router_ids = {
    'NewYork': '1.1.1.1',
    'Montana': '2.2.2.2',
    'Virginia': '3.3.3.3',
    'Texas': '4.4.4.4',
    'Arizona': '5.5.5.5',
    'Florida': '6.6.6.6'
}

# Iterate over devices in the testbed
for device_name, device_object in testbed.devices.items():
    dev = device_object
    
    # Connect to the device
    dev.connect(log_stdout=False)
    
    # Parse the OSPF information
    ospf_neighbors = dev.parse("show ip ospf")['vrf']['default']['address_family']['ipv4']['instance']
    
    for instance_key in ospf_neighbors:
        router_id = ospf_neighbors[instance_key].get('router_id')
        
        # Assert that the retrieved router ID matches the expected router ID
        expected_id = expected_router_ids.get(device_name)
        
        if router_id == expected_id:
            pprint(f"✔️ Router {device_name} Instance {instance_key} has correct Router ID: {router_id}")
        else:
            pprint(f"❌ Router {device_name} Instance {instance_key} has incorrect Router ID: {router_id} (Expected: {expected_id})")
            
    # Optionally, disconnect from the device after collecting the required data
    dev.disconnect()
