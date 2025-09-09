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

            # Ignore "parent directory" or anchors
            if href.startswith("?") or href.startswith("#") or href.startswith("../"):
                continue

            # Detect if it's a folder
            is_dir = href.endswith("/")
            filename = href.rstrip("/").split("/")[-1]

            # Skip HTML/PHP/ASP/etc. pages that aren’t real hosted files
            if not is_dir and re.search(r"\.(php|html?|asp|aspx|jsp)$", filename, re.I):
                continue

            # Guess type
            if is_dir:
                ftype = "Directory"
            elif "." in filename:
                ftype = f".{filename.split('.')[-1]} file"
            else:
                ftype = "File"

            # Try to extract file size + modified date if available in listing row
            row_text = link.parent.get_text(" ", strip=True)
            size_match = re.search(r"(\d+(?:\.\d+)?\s*(?:KB|MB|GB|B))", row_text, re.I)
            date_match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2})", row_text)

            size = size_match.group(1) if size_match else "-"
            modified = date_match.group(1) if date_match else "-"

            files.append((filename, ftype, size, modified))

        if not files:
            print(Fore.YELLOW + "No files or directories found (maybe directory listing is disabled)." + Style.RESET_ALL)
            return

        print(Fore.GREEN + "\nFiles found:" + Style.RESET_ALL)
        print(Fore.MAGENTA + f"{'Name':<30}{'Type':<15}{'Size':<12}{'Modified':<20}" + Style.RESET_ALL)
        print(Fore.MAGENTA + "-" * 77 + Style.RESET_ALL)

        for fname, ftype, size, modified in files:
            if ftype == "Directory":
                color = Fore.BLUE
            elif ftype.endswith("file"):
                color = Fore.CYAN
            else:
                color = Fore.WHITE

            print(f"{color}{fname:<30}{Style.RESET_ALL} "
                  f"{Fore.WHITE}{ftype:<15}{size:<12}{modified:<20}{Style.RESET_ALL}")
