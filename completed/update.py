import requests
from bs4 import BeautifulSoup
import time
import hashlib
import argparse
from viv import sayt
def fetch_website_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the website: {e}")
        return None
# Function to monitor changes
def monitor_website(url, interval):
    print(f"Monitoring website: {url}")
    previous_hash = None
    while True:
        content = fetch_website_content(url)
        if content:
            current_hash = hashlib.md5(content.encode('utf-8')).hexdigest()  # Create a hash of the content
            if previous_hash is None:
                previous_hash = current_hash
            elif current_hash != previous_hash:
                print(f"Change detected on {url}!")
                sayt("update detected!")
                previous_hash = current_hash
        time.sleep(interval)  # Wait for the specified interval
parser = argparse.ArgumentParser()
parser.add_argument("site", nargs='?', help="the url to chack for updates")
args = parser.parse_args()
if args.site == None:
    websitetm = input("what site do you want to monitor \n> ")
    if websitetm.startswith("http") == False:
        websitetm = "https://" + websitetm
else:
    websitetm = args.site

monitor_website(websitetm, 1)