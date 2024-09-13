from nornir import InitNornir # <-- This turns the nornir engine on
from nornir_scrapli.tasks import send_command # <-- Send show commands utilizing scrapli
from nornir_utils.plugins.functions import print_result # <-- Print our results to the terminal
from nornir_utils.plugins.tasks.files import write_file

nr = InitNornir(config_file='config.yaml')

def save_config(task):
    task.run(task=send_command, command="copy run start\n")

results = nr.run(task=save_config)
print_result(results)





