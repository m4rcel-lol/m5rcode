import os, requests
from utils.downloader import download_and_extract
from pathlib import Path

def check_and_update():
    remote_ver = requests.get("https://yourserver.com/version.txt").text.strip()
    local_ver = Path(__file__).parents[2].joinpath("version.txt").read_text().strip()
    if remote_ver != local_ver:
        print("Updating to", remote_ver)
        download_and_extract("https://yourserver.com/m5rcode.zip", os.path.dirname(__file__))
        Path(__file__).parents[2].joinpath("version.txt").write_text(remote_ver)
        print("Update complete!")
    else:
        print("Already up to date.")
