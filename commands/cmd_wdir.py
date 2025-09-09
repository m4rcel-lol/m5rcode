import requests
from bs4 import BeautifulSoup
from colorama import Fore

class WdirCommand:
    def __init__(self, url):
        self.url = url.strip()

    def run(self):
        if not self.url:
            print(Fore.RED + "Usage: wdir <url>")
            return

        if not self.url.startswith("http://") and not self.url.startswith("https://"):
            self.url = "http://" + self.url

        try:
            response = requests.get(self.url, timeout=5)
            if response.status_code != 200:
                print(Fore.RED + f"Failed to fetch URL (status {response.status_code})")
                return

            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a")

            files = []
            dirs = []

            for link in links:
                href = link.get("href")
                if not href or href.startswith("?") or href.startswith("#"):
                    continue
                if href in ("../", "/"):
                    continue  # skip parent link
                if href.endswith("/"):
                    dirs.append(href)
                else:
                    files.append(href)

            if not files and not dirs:
                print(Fore.YELLOW + "No directory listing found (site may not expose files).")
                return

            print(Fore.CYAN + f"Directory listing for {self.url}:\n")

            for d in dirs:
                print(Fore.BLUE + f"[DIR]  {d}")
            for f in files:
                print(Fore.GREEN + f"[FILE] {f}")

        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"Error fetching URL: {e}")
