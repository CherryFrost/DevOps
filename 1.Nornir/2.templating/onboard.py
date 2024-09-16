"Configure physical gig interfaces"
from nornir import InitNornir
from nornir_scrapli.tasks import send_configs
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_file


nr = InitNornir(config_file='config.yaml')

target_device = nr.filter(country="usa")

def load_vars(task):
    """Load variables from a YAML file into the task host's facts."""
    data = task.run(task=load_yaml, file=f"./1.host_vars/{task.host}.yaml")
    task.host['facts'] = data.result
    onboard(task)

def onboard(task):
    """Render a Jinja2 template and apply the resulting configuration to the device."""
    template = task.run(task=template_file, template="onboard.j2", path="2.templating/templates")
    task.host["onboard_config"] = template.result
    rendered = task.host["onboard_config"]
    configuration = rendered.splitlines()
    task.run(task=send_configs, configs=configuration)


results = nr.run(task=load_vars)
print_result(results)
