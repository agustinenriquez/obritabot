import requests
from bs4 import BeautifulSoup
import time
import random
import os
from datetime import datetime, timedelta

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    # Add more user agents
]

LAST_RUN_FILE = "tests/last_run_timestamp.txt"
CACHE_FILE = "tests/cac_cache.txt"

def should_run_test():
    if os.path.exists(LAST_RUN_FILE):
        with open(LAST_RUN_FILE, "r") as f:
            last_run_timestamp = f.read().strip()
            last_run_time = datetime.strptime(last_run_timestamp, "%Y-%m-%d %H:%M:%S")
            if datetime.now() - last_run_time < timedelta(days=1):
                return False
    return True

def update_last_run_timestamp():
    with open(LAST_RUN_FILE, "w") as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def cache_cac_value(cac_value):
    with open(CACHE_FILE, "w") as f:
        f.write(cac_value)

def get_cached_cac_value():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return f.read().strip()
    return None

def scrape_cac_index_alternative():
    if not should_run_test():
        cached_value = get_cached_cac_value()
        if cached_value:
            print(f"Using cached CAC Index: {cached_value}")
            return cached_value
        else:
            print("Test already run within the last 24 hours, but no cached value found. Scraping new value.")
    
    url = "https://ikiwi.net.ar/indice-cac/"
    headers = {
        'User-Agent': random.choice(user_agents)
    }
    response = requests.get(url, headers=headers)
    time.sleep(1)  # Sleep for 1 second between requests
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find the CAC index in the <span id="cacHoy"> element
        cac_index_element = soup.find('span', id='cacHoy')
        if cac_index_element:
            cac_index = cac_index_element.text.strip()
            update_last_run_timestamp()
            cache_cac_value(cac_index)
            return cac_index
        else:
            print("CAC index element not found.")
            return None
    else:
        print(f"Failed to fetch the page, status code: {response.status_code}")
        return None

if __name__ == "__main__":
    cac_index = scrape_cac_index_alternative()
    if cac_index:
        print(f"CAC Index from ikiwi: {cac_index}")
    else:
        print("Failed to scrape CAC Index from ikiwi")