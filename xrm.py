import os
import time
import requests
from http.cookiejar import MozillaCookieJar
from rich.panel import Panel
from rich import print as printf
from requests.exceptions import RequestException

COOKIE_FILE = "cookie.txt"  # Ensure it's in the same directory
MAX_RUNTIME = 21500  # 5 hours, 58 minutes (just before GitHub Actions stops it)
start_time = time.time()

def load_netscape_cookies(file_path):
    if not os.path.exists(file_path):
        printf(Panel("[bold red]Cookie file not found! Waiting...", style="bold bright_black", width=56))
        while not os.path.exists(file_path):
            time.sleep(10)
    cookie_jar = MozillaCookieJar(file_path)
    cookie_jar.load(ignore_discard=True, ignore_expires=True)
    return cookie_jar

class CLAIM:
    def __init__(self, cookies):
        self.cookies = cookies

    def EXECUTION(self):
        with requests.Session() as r:
            r.cookies = self.cookies
            r.headers.update({
                'User-Agent': 'Mozilla/5.0 (Linux; Android 14; RMX3706)',
                'Referer': 'https://faucetearner.org/dashboard.php',
                'Host': 'faucetearner.org',
            })
            response2 = r.post('https://faucetearner.org/api.php?act=faucet', data={})
            if 'congratulations' in response2.text.lower():
                printf(Panel("[italic green]Claim successful!", style="bold bright_black", width=56))
            elif 'you have already' in response2.text.lower():
                printf(Panel("[bold red]Already claimed, waiting...", style="bold bright_black", width=56))
            else:
                printf(Panel(f"[bold red]{response2.text}", style="bold bright_black", width=56))

    def XRP(self):
        while True:
            if time.time() - start_time > MAX_RUNTIME:
                printf(Panel("[bold yellow]Time limit reached. Restarting script...", style="bold bright_black", width=56))
                os.system("git pull && nohup python xrp.py &")  # Restart
                exit()
            try:
                self.EXECUTION()
                time.sleep(62)
            except RequestException:
                printf("[bold red]Connection issue! Retrying...")
                time.sleep(10)

if __name__ == '__main__':
    cookies = load_netscape_cookies(COOKIE_FILE)
    CLAIM(cookies).XRP()
