from nornir import InitNornir
from nornir_scrapli.tasks import send_configs
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file
from nornir.core.filter import F
from nornir_utils.plugins.tasks.data import load_yaml

nr = InitNornir(config_file='config.yaml')

target_device = nr.filter(F(tag="snell"))
# print(target_device.inventory.hosts.keys())


def load_vars(task):
    data = task.run(task=load_yaml, file=f"./1.host_vars/{task.host}.yaml")
    task.host['facts'] = data.result
    port_security(task)


def port_security(task):
    template = task.run(task=template_file, template="switch1.j2", path="2.templating/templates")
    task.host["port_sec"] = template.result
    rendered = task.host["port_sec"]
    configuration = rendered.splitlines()
    task.run(task=send_configs, configs=configuration)


results = target_device.run(task=load_vars)
print_result(results)