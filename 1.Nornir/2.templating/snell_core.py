from nornir import InitNornir
from nornir_scrapli.tasks import send_configs
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml

nr = InitNornir(config_file='config.yaml')
target_device = nr.filter(tag='snell')

def load_vars(task):
    data = task.run(task=load_yaml, file=f"./1.host_vars/{task.host}.yaml")
    task.host['facts'] = data.result
    build_inital_config(task)

def build_inital_config(task):
    template = task.run(task=template_file, template="snell_core.j2", path="2.templating/templates")
    task.host['day1'] = template.result
    rendered = task.host['day1']
    configuration = rendered.splitlines()
    task.run(task=send_configs, configs=configuration)

results = target_device.run(task=load_vars)
print_result(results)