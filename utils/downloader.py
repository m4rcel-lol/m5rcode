import requests, zipfile, io

def download_and_extract(url, target_dir):
    resp = requests.get(url)
    resp.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
        z.extractall(target_dir)
