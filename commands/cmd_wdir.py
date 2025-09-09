import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from colorama import Fore, Style
import re

class WdirCommand:
    def __init__(self, url):
        self.url = url.strip()

    def run(self):
        if not self.url:
            print(Fore.RED + "Usage: wdir <url>" + Style.RESET_ALL)
            return

        # Ensure scheme
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

            filename = href.split("/")[-1]
            full_url = urljoin(self.url, href)

            # Guess type
            if "." in filename:
                ext = filename.split(".")[-1].lower()
                ftype = f".{ext} file"
            else:
                ftype = "Directory"

            # Try to extract file size and modified date from raw HTML
            row_text = link.parent.get_text(" ", strip=True)
            size_match = re.search(r"(\d+(?:\.\d+)?\s*(?:KB|MB|GB|B))", row_text, re.I)
            date_match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2})", row_text)

            size = size_match.group(1) if size_match else "?"
            modified = date_match.group(1) if date_match else "?"

            files.append((filename, ftype, size, modified, full_url))

        if not files:
            print(Fore.YELLOW + "No files or directories found (maybe directory listing is disabled)." + Style.RESET_ALL)
            return

        print(Fore.GREEN + "\nFiles found:" + Style.RESET_ALL)
        print(Fore.MAGENTA + f"{'Name':<30}{'Type':<15}{'Size':<12}{'Modified':<20}" + Style.RESET_ALL)
        print(Fore.MAGENTA + "-" * 77 + Style.RESET_ALL)

        for fname, ftype, size, modified, furl in files:
            print(f"{Fore.CYAN}{fname:<30}{Style.RESET_ALL} "
                  f"{Fore.WHITE}{ftype:<15}{size:<12}{modified:<20}{Style.RESET_ALL}")
