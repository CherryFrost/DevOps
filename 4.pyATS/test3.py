# allow testbed to be loaded in
from genie.testbed import load
from rich import print as pprint

testbed = load('testbed.yaml')
device_one = testbed.devices['R1-NewYork']

# minimize log output on screen when running test
device_one.connect(log_stdout=False)

parsed_intf = device_one.parse("show ip int brief")
mgmt_ipAddr = parsed_intf['interface']['GigabitEthernet0/0']['ip_address']
vers_parse = device_one.parse("show version")
hostname = vers_parse['version']['hostname']

pprint(f"[yellow]Device:[/yellow] {hostname} [purple]has a management IP of:[/purple] [yellow]{mgmt_ipAddr}[/yellow]")
