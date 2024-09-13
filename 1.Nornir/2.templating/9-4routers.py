from nornir import InitNornir
from nornir_scrapli.tasks import send_configs
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml

# Initialize nornir from config.yaml
nr = InitNornir(config_file='config.yaml')

# Filter only routers in lab
usa_routers = nr.filter(country="usa")

# Confirm filtering is targeting the correct devices - Uncomment line 14 to test
#print(usa_routers.inventory.hosts.keys())

#funtion to load host vars found in: ./host_vars
def load_host_vars(task):
    data = task.run(task=load_yaml, file=f"./1.host_vars/{task.host}.yaml")
    task.host['facts'] = data.result
# call below funtions to execute after host vars have been loaded
    configure_loopbacks(task)
    configure_physical_intf(task)
    configure_ospf(task)

def configure_loopbacks(task):
    template = task.run(task=template_file, template="lan.j2", path="2.templating/templates")
    task.host['loopbacks'] = template.result
    rendered = task.host['loopbacks']
    configuration = rendered.splitlines()
    task.run(task=send_configs, configs=configuration)

def configure_physical_intf(task):
    template = task.run(task=template_file, template="onboard.j2", path="6.templating/templates")
    task.host['phys_intf'] = template.result
    rendered = task.host['phys_intf']
    configuration = rendered.splitlines()
    task.run(task=send_configs, configs=configuration)

def configure_ospf(task):
    template = task.run(task=template_file, template="ospf.j2", path="6.templating/templates")
    task.host['phys_intf'] = template.result
    rendered = task.host['phys_intf']
    configuration = rendered.splitlines()
    task.run(task=send_configs, configs=configuration)

# print complete output to terminal
results = usa_routers.run(task=load_host_vars)
print_result(results)