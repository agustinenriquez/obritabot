import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

def scrape_news():
    today = datetime.now().strftime('%Y-%m-%d')
    flag_file = '/home/m0tz/obritabot/backend/scrape_flag.txt'

    if os.path.exists(flag_file):
        with open(flag_file, 'r') as file:
            last_scraped = file.read().strip()
        if last_scraped == today:
            print("News already scraped today. Skipping...")
            return

    url = "https://www.ambito.com/construccion-a5122808"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        news_items = soup.find_all('div', class_='article-content')
        for item in news_items:
            title = item.find('h2').get_text(strip=True)
            summary = item.find('p').get_text(strip=True)
            print(f"Title: {title}")
            print(f"Summary: {summary}")
            print("-" * 40)
        with open(flag_file, 'w') as file:
            file.write(today)
    else:
        print("Failed to retrieve the news")

if __name__ == "__main__":
    scrape_news()
