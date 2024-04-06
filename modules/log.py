import os
from datetime import datetime
from pathlib import Path
resources_path = Path("resources")
log_path = resources_path / "log.txt"
generated_path = resources_path / "generated.txt"
os.system("color")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def logGenerated(id, name) -> None:
    time = datetime.strftime(datetime.now(),"%H:%M:%S")
    date = datetime.today().strftime('%d-%m-%y')
    with open(generated_path,"a") as f:
        f.write(f"[{date} [{time}] {name} - https://roblox.com/groups/{id}")
    f.close()

def logSuccess(message:str) -> None:
    time = datetime.strftime(datetime.now(),"%H:%M:%S")
    date = datetime.today().strftime('%d-%m-%y')
    print(f"{bcolors.OKGREEN}[{date}] [{time}] [Success] {message}")
    with open(log_path,"a") as f:
        f.write(f"[{date}] [{time}] [Success] {message}\n")
    f.close()

def logWarning(message:str) -> None:
    time = datetime.strftime(datetime.now(),"%H:%M:%S")
    date = datetime.today().strftime('%d-%m-%y')
    print(f"{bcolors.WARNING}[{date}] [{time}] [Warning] {message}")
    with open(log_path,"a") as f:
        f.write(f"[{date}] [{time}] [Warning] {message}\n")
    f.close()

def logError(message:str) -> None:
    time = datetime.strftime(datetime.now(),"%H:%M:%S")
    date = datetime.today().strftime('%d-%m-%y')
    print(f"{bcolors.FAIL}[{date}] [{time}] [Error] {message}")
    with open(log_path,"a") as f:
        f.write(f"[{date}] [{time}] [Error] {message}\n")
    f.close()

def logInfo(message:str) -> None:
    time = datetime.strftime(datetime.now(),"%H:%M:%S")
    date = datetime.today().strftime('%d-%m-%y')
    print(f"{bcolors.OKCYAN}[{date}] [{time}] [Info] {message}")
    with open(log_path,"a") as f:
        f.write(f"[{date}] [{time}] [Info] {message}\n")
    f.close()