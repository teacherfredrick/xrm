import os
import time
import sys
import subprocess

# Ensure required modules are installed
REQUIRED_MODULES = ["requests", "rich"]

def install_missing_modules():
    for module in REQUIRED_MODULES:
        try:
            __import__(module)
        except ImportError:
            print(f"Installing missing module: {module}")
            subprocess.run([sys.executable, "-m", "pip", "install", module])

install_missing_modules()

import requests
from http.cookiejar import MozillaCookieJar
from rich.panel import Panel
from rich import print as printf
from requests.exceptions import RequestException

# Use a dynamic path for the cookie file
COOKIE_FILE = os.path.expanduser("~/cookie.txt")  

def load_netscape_cookies(file_path):
    """Loads cookies from a Netscape-format file."""
    if not os.path.exists(file_path):
        printf(Panel("[bold red]Cookie file not found! Waiting for upload...", style="bold bright_black", width=56))
        while not os.path.exists(file_path):  # Keep waiting for the file
            time.sleep(10)
    cookie_jar = MozillaCookieJar(file_path)
    cookie_jar.load(ignore_discard=True, ignore_expires=True)
    return cookie_jar

def BANNER():
    os.system('cls' if os.name == 'nt' else 'clear')
    printf(Panel(r"""[bold red]●[bold yellow] ●[bold green] ●[/]
[bold red]    ______                      __                 
   / ____/___ ___  __________  / /____  ____ ______
  / /_  / __ `/ / / / ___/ _ \/ __/ _ \/ __ `/ ___/
 / __/ / /_/ / /_/ / /__/  __/ /_/  __/ /_/ / /    
[bold white]/_/    \__,_/\__,_/\___/\___/\__/\___/\__,_/_/     
        [bold white on red]Free XRP Tokens - Auto-Running""", style="bold bright_black", width=56))

class CLAIM:
    def __init__(self, cookies) -> None:
        self.cookies = cookies

    def EXECUTION(self):
        with requests.Session() as r:
            r.cookies = self.cookies  # Attach the Netscape cookies

            r.headers.update({
                'User-Agent': 'Mozilla/5.0 (Linux; Android 14; RMX3706 Build/UKQ1.230924.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36',
                'Referer': 'https://faucetearner.org/dashboard.php',
                'Host': 'faucetearner.org',
            })

            response = r.get('https://faucetearner.org/faucet.php')
            response2 = r.post('https://faucetearner.org/api.php?act=faucet', data={})

            if 'congratulations' in str(response2.text).lower():
                printf(Panel("[italic green]Claim successful!", style="bold bright_black", width=56))
            elif 'you have already' in str(response2.text).lower():
                printf(Panel("[bold red]Already claimed, please wait!", style="bold bright_black", width=56))
            else:
                printf(Panel(f"[bold red]{str(response2.text)}", style="bold bright_black", width=56))

    def XRP(self):
        BANNER()
        printf(Panel("[bold white]Claiming XRP... Press STOP button to end.", style="bold bright_black", width=56))
        while True:
            try:
                self.EXECUTION()
                printf("[bold cyan]Waiting 62 seconds before the next claim...")
                time.sleep(62)
            except RequestException:
                printf("[bold red]Connection issue! Retrying...")
                time.sleep(10)

def run_forever():
    """Ensures the script runs indefinitely, restarting if it stops."""
    retries = 0
    while True:
        try:
            os.system('git pull')  # Update the script if stored in GitHub
            cookies = load_netscape_cookies(COOKIE_FILE)
            CLAIM(cookies).XRP()
        except Exception as e:
            retries += 1
            printf(Panel(f"[bold red]Error: {str(e)}. Restarting (Attempt {retries})...", style="bold bright_black", width=56))
            time.sleep(min(60 * retries, 600))  # Increase wait time on multiple failures

if __name__ == '__main__':
    run_forever()
