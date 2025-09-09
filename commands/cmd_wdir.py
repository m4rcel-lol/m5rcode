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

            if not links:
                print(Fore.YELLOW + "No directory listing or links found at this URL.")
                return

            print(Fore.CYAN + f"Directory listing for {self.url}:\n")
            for link in links:
                href = link.get("href")
                if href:
                    print(Fore.GREEN + " - " + href)

        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"Error fetching URL: {e}")
