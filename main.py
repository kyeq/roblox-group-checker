from modules import roblox
from modules import log
import random
import string
import json
import time

config_file = open("config.json") 
config_data = json.load(config_file)

refresh_rate = config_data['rate']

cached = []

def random_name(Length=2):
    Letters = string.ascii_lowercase
    return ''.join(random.choice(Letters) for _ in range(Length))

## get csrf for authentication
x_csrf_token = roblox.get_csrf_token()

log.logInfo("Group generator started.")

## begin making requests!
while True:
    next_name = random_name()
    
    if next_name not in cached:
        cached.append(next_name)

        creation = roblox.create_group(name=next_name, csrf_token=x_csrf_token)
        
        if 'error' in creation:
            log.logError('An error occured when making the request: {}'.format(creation['error']))
            break
        elif 'errors' in creation:
            log.logInfo("Tried '{}' - unavailable!".format(next_name))
        elif 'id' in creation:
            log.logSuccess("Created group '{}' / {}".format(creation['name'], creation['id']))
            log.logGenerated(creation['id'], creation['name'])
        
        time.sleep(refresh_rate)

log.logInfo("Group generator stopped.")