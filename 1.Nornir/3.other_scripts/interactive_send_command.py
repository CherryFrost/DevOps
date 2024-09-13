from nornir import InitNornir # <-- This turns the nornir engine on
from nornir_scrapli.tasks import send_command # <-- Send show commands utilizing scrapli
from nornir_utils.plugins.functions import print_result # <-- Print our results to the terminal

nr = InitNornir(config_file='config.yaml')

while True:
    # Prompt the user for a command
    command = input("Please enter the command you would like to send: ")
    
    # Execute the command and print the results
    results = nr.run(task=send_command, command=command)
    print_result(results)
    
    # Ask the user if they want to enter another command
    next_command = input("Would you like to enter another command? (y/n): ")
    
    # Break the loop if the user does not want to enter another command
    if next_command.lower() != 'y':
        print("=" * 24)
        print("Exiting the devnet zone.".upper())
        print("=" * 24)
        break