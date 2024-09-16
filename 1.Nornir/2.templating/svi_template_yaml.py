import os
from nornir import InitNornir
from nornir_scrapli.tasks import send_configs
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file
from nornir.core.filter import F
from nornir_utils.plugins.tasks.data import load_yaml

nr = InitNornir(config_file='config.yaml')
nr.inventory.defaults.username = os.getenv("SSH_USERNAME")
nr.inventory.defaults.password = os.getenv("SSH_PASSWORD")

target_device = nr.filter(F(groups__contains="Mgmt_group"))


def load_vars(task):
    data = task.run(task=load_yaml, file=f"./1.host_vars/{task.host}.yaml")
    task.host['facts'] = data.result
    svi_templates(task)


def svi_templates(task):
    template = task.run(task=template_file, template="svi.j2", path="2.templating/templates")
    task.host["svi_config"] = template.result
    rendered = task.host["svi_config"]
    configuration = rendered.splitlines()
    task.run(task=send_configs, configs=configuration)


results = target_device.run(task=load_vars)
print_result(results)