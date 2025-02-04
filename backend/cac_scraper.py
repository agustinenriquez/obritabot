import requests
from bs4 import BeautifulSoup
import time
import random

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    # Add more user agents
]


def scrape_cac_index_alternative():
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
            return cac_index
        else:
            print("CAC index element not found.")
            return None
    else:
        print(f"Failed to fetch the page, status code: {response.status_code}")
        return None

if __name__ == "__main__":
    cac_index = scrape_cac_index()
    if cac_index:
        print(f"CAC Index from cifrasonline: {cac_index}")
    else:
        print("Failed to scrape CAC Index from cifrasonline")

    cac_index_alternative = scrape_cac_index_alternative()
    if cac_index_alternative:
        print(f"CAC Index from ikiwi: {cac_index_alternative}")
    else:
        print("Failed to scrape CAC Index from ikiwi")