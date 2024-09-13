from nornir import InitNornir # <-- This turns the nornir engine on
from nornir_scrapli.tasks import send_command # <-- Send show commands utilizing scrapli
from nornir_utils.plugins.functions import print_result # <-- Print our results to the terminal
from nornir_utils.plugins.tasks.files import write_file
from datetime import date
import pathlib

nr = InitNornir(config_file='config.yaml')

def backup_config(task):
    r = task.run(task=send_command, command="show run")
    config_archive = "backups"
    date_dir = config_archive + "/" + str(date.today())
    pathlib.Path(date_dir).mkdir(exist_ok=True)
    task.run(task=write_file, content=r.result, filename=str(date_dir) + f"/{task.host}.txt") # <-- '.result' is what allows us to get the contents of that variable

results = nr.run(task=backup_config)
