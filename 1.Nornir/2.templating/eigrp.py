import os
from nornir import InitNornir
from nornir_scrapli.tasks import send_configs
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml

nr = InitNornir(config_file='config.yaml')
nr.inventory.defaults.username = os.getenv("SSH_USERNAME")
nr.inventory.defaults.password = os.getenv("SSH_PASSWORD")

target_device = nr.filter(state="newyork")

def load_vars(task):
    data = task.run(task=load_yaml, file=f"./1.host_vars/{task.host}.yaml")
    task.host['facts'] = data.result
    build_eigrp(task)

# Build eigrp AS 15 -> R1 and R5
def build_eigrp(task):
    template = task.run(task=template_file, template="eigrp.j2", path="2.templating/templates")
    task.host['eigrp_config'] = template.result
    rendered = task.host['eigrp_config']
    configuration = rendered.splitlines()
    task.run(task=send_configs, configs=configuration)

results = target_device.run(task=load_vars)
print_result(results)