import requests
import json
from modules import log 

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
        return 9999999#robux_value
    except KeyError:
        log.logError("Couldn't get robux stock via Roblox api. Invalid Roblox cookie?\n( {} )".format(str(urlHandler.json())))
    except Exception as error:
        log.logError("Couldn't get robux stock via Roblox api. Invalid Roblox cookie?\n( {} ) [{}]".format(str(urlHandler.json),str(error)))

def get_gamepass_info(gamepass_id):
    log.logInfo("Fetching gamepass info, for ID {}.".format(gamepass_id))
    try:
        gamepass_params = {
            "gamePassId": str(gamepass_id)
        }
        urlHandler = requests.get("http://api.roblox.com/marketplace/game-pass-product-info/",params=gamepass_params,headers=HEADERS).json()
        product_info = {
            "ProductId": urlHandler["ProductId"],
            "PriceInRobux": urlHandler["PriceInRobux"],
            "CreatorTargetId": urlHandler["Creator"]["CreatorTargetId"],
            "success": True
        }
        log.logSuccess("Successfully fetched gamepass info, for ID {}.".format(gamepass_id))
        return product_info
    except IndexError:
        log.logWarning("Gamepass does not exist, for ID {}.".format(gamepass_id))
        product_info = {
            "success": False
        }
        return product_info
    except Exception as error:
        log.logError("Couldn't check whether gamepass exists, for ID {}. '{}'".format(gamepass_id,str(error)))
        product_info = {
            "success": False
        }
        return product_info

def get_csrf_token():
    log.logInfo("Attempting to fetch roblox x-csrf-token...")
    try:
        session_cookies = {'.ROBLOSECURITY': roblox_security_cookie}
        csrf = requests.post("https://auth.roblox.com/v2/logout",headers=HEADERS,cookies=session_cookies).headers["x-csrf-token"]
        log.logSuccess("Successfully fetched roblox x-csrf-token.")
        return csrf
    except Exception as error:
        log.logError("Couldn't fetch roblox x-csrf-token. '{}'".format(str(error)))

def buy_gamepass(gamepass_data):
    log.logInfo("Attempting to purchase gamepass...")
    try:
        csrf = get_csrf_token()
        session_cookies = {'.ROBLOSECURITY': roblox_security_cookie}
        data = {"expectedCurrency": 1, "expectedPrice": gamepass_data["ExpectedPrice"], "expectedSellerId": gamepass_data["CreatorTargetId"]}
        headers = {"X-CSRF-TOKEN": csrf}
        purchase = requests.post("https://economy.roblox.com/v1/purchases/products/{}".format(gamepass_data["ProductId"]),data=data,headers=headers,cookies=session_cookies).json()
        log.logSuccess("Successfully purchased gamepass, for ID {}.".format(gamepass_data["ProductId"]))
        log.logInfo("Attempting to delete product from inventory...")
        deletion = requests.post("https://www.roblox.com/game-pass/revoke",data={"id":gamepass_data["ProductId"]},headers={"X-CSRF-TOKEN":csrf},cookies=session_cookies)
        log.logSuccess("Successfully deleted product from inventory.")
        return purchase
    except Exception as error:
        log.logError("Couldn't purchase gamepass! '{}'".format(str(error)))
        