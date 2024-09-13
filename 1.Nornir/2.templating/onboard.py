from nornir import InitNornir
from nornir_scrapli.tasks import send_configs
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml

nr = InitNornir(config_file='config.yaml')

target_device = nr.filter(state="newyork")


def load_vars(task):
    data = task.run(task=load_yaml, file=f"./1.host_vars/{task.host}.yaml")
    task.host['facts'] = data.result
    onboard(task)


def onboard(task):
    template = task.run(task=template_file, template="onboard.j2", path="2.templating/templates")
    task.host["onboard_config"] = template.result
    rendered = task.host["onboard_config"]
    configuration = rendered.splitlines()
    task.run(task=send_configs, configs=configuration)


results = nr.run(task=load_vars)
print_result(results)