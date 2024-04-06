import requests
import json
from modules import log
import datetime

config_file = open("config.json") 
config_data = json.load(config_file)
roblox_security_cookie = config_data['roblox-auth-token']

HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'})

def get_robux_value():
    log.logInfo("Attempting to get robux stock via Roblox api.")
    session_cookies = {'.ROBLOSECURITY': roblox_security_cookie}
    try:
        urlHandler = requests.get("https://economy.roblox.com/v1/user/currency",headers=HEADERS,cookies=session_cookies)
        robux_value = urlHandler.json()['robux']
        log.logSuccess("Successfully fetched robux stock via Roblox api: {}".format(robux_value))
        return robux_value
    except KeyError:
        log.logError("Couldn't get robux stock via Roblox api. Invalid Roblox cookie?\n( {} )".format(str(urlHandler.json())))
    except Exception as error:
        log.logError("Couldn't get robux stock via Roblox api. Invalid Roblox cookie?\n( {} ) [{}]".format(str(urlHandler.json),str(error)))

def get_csrf_token():
    log.logInfo("Attempting to fetch roblox x-csrf-token...")
    try:
        session_cookies = {'.ROBLOSECURITY': roblox_security_cookie}
        csrf = requests.post("https://auth.roblox.com/v2/logout",headers=HEADERS,cookies=session_cookies).headers["x-csrf-token"]
        log.logSuccess("Successfully fetched roblox x-csrf-token.")
        return csrf
    except Exception as error:
        log.logError("Couldn't fetch roblox x-csrf-token. '{}'".format(str(error)))

def create_group(name: str, csrf_token: str) -> bool:
    """
    Attemps to create a group with the given name.

    Parameters:
    name (str): The name of the group to create.
    csrf_token (str): The csrf authentication token.
    """

    current_datetime = datetime.datetime.now()
    formatted_date_time = current_datetime.strftime("%d/%m/%Y - %H:%M")

    files = {
        "icon": open("./group_icon.png", "rb")
    }

    data = {
        "name": name,
        "description": "[Auto made on {} - GG!]".format(formatted_date_time),
        "publicGroup": True
    }

    session_cookies = {'.ROBLOSECURITY': roblox_security_cookie}

    headers = {"X-CSRF-TOKEN": csrf_token}

    try:
        response = requests.post('https://groups.roblox.com/v1/groups/create', headers=headers, data=data, files=files, cookies=session_cookies)
        return response.json()
    except any as error:
        return json.dump({'error': str(error)})