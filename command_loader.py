import requests
import yaml
import os



# token key
BOT_TOKEN = os.getenv('DISCORD_TOKEN')

# Channel ID
CHANNEL_ID = os.getenv('CHANNEL_ID')
#Application ID
APPLICATION_ID = os.getenv('APPLICATION_ID')
#Url
URL = f"https://discord.com/api/v9/applications/{APPLICATION_ID}/commands"

with open('commands.yml') as file:
    yaml_content = file.read()


commands = yaml.safe_load(yaml_content)

headers = {"Authorization": f"Bot {BOT_TOKEN}", "Content-Type": "application/json"}

# Delete existing commands
response = requests.get(URL, headers=headers)

list = """
1. Delete all commands
2. Delete specific command
3. Add new commands
4. Exit
"""
input = int(input(list))

if input == 1:
    for command in response.json():
        command_id = command['id']
        response = requests.delete(f"{URL}/{command_id}", headers=headers)
        print(f"Command {command_id} has been deleted with status code {response.status_code}")

elif input == 2:
    command_name = input("Enter the command name to delete: ")
    for command in response.json():
        if command['name'] == command_name:
            command_id = command['id']
            response = requests.delete(f"{URL}/{command_id}", headers=headers)
            print(f"Command {command_id} has been deleted with status code {response.status_code}")
            break
    else:
        print(f"Command {command_name} not found.")

elif input == 3:
    for command in commands:
        response = requests.post(URL, headers=headers, json=command)
        print(f"Command {command['name']} has been added with status code {response.status_code}")

else:
    print("Exiting...")
    exit(0)