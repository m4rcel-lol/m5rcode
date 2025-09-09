import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from colorama import Fore, Style

class WdirCommand:
    def __init__(self, url):
        self.url = url.strip()

    def run(self):
        if not self.url:
            print(Fore.RED + "Usage: wdir <url>" + Style.RESET_ALL)
            return

        # Ensure URL has scheme
        if not self.url.startswith("http://") and not self.url.startswith("https://"):
            self.url = "http://" + self.url

        try:
            print(Fore.CYAN + f"[FETCH] Scanning directory at {self.url}..." + Style.RESET_ALL)
            resp = requests.get(self.url, timeout=5)
            resp.raise_for_status()
        except Exception as e:
            print(Fore.RED + f"[ERR] Failed to fetch {self.url}: {e}" + Style.RESET_ALL)
            return

        soup = BeautifulSoup(resp.text, "html.parser")
        links = soup.find_all("a")

        files = []
        for link in links:
            href = link.get("href")
            if not href:
                continue

            # Skip parent directory and in-page anchors
            if href.startswith("?") or href.startswith("#") or href == "../":
                continue

            full_url = urljoin(self.url, href)
            filename = href.split("/")[-1]

            # Determine file type
            if "." in filename:
                ext = filename.split(".")[-1].lower()
                ftype = f".{ext} file"
            else:
                ftype = "Directory"

            files.append((filename, ftype, full_url))

        if not files:
            print(Fore.YELLOW + "No files or directories found (maybe directory listing is disabled)." + Style.RESET_ALL)
            return

        print(Fore.GREEN + "\nFiles found:" + Style.RESET_ALL)
        for fname, ftype, furl in files:
            print(f"  {Fore.CYAN}{fname:<30}{Style.RESET_ALL} {Fore.WHITE}→ {ftype}{Style.RESET_ALL}")
