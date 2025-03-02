import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import sqlite3

def init_db():
    conn = sqlite3.connect('/home/m0tz/obritabot/backend/news_cache.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            date TEXT PRIMARY KEY,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_news_to_db(date, content):
    conn = sqlite3.connect('/home/m0tz/obritabot/backend/news_cache.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO news (date, content) VALUES (?, ?)', (date, content))
    conn.commit()
    conn.close()

def get_news_from_db(date):
    conn = sqlite3.connect('/home/m0tz/obritabot/backend/news_cache.db')
    cursor = conn.cursor()
    cursor.execute('SELECT content FROM news WHERE date = ?', (date,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def scrape_news():
    flag_file = '/home/m0tz/obritabot/backend/scrape_flag.txt'
    today = datetime.now().strftime('%Y-%m-%d')

    # Check if the flag file exists and contains today's date
    if os.path.exists(flag_file):
        with open(flag_file, 'r') as f:
            if f.read().strip() == today:
                print("News already scraped today. Skipping...")
                return

    cached_news = get_news_from_db(today)
    if cached_news:
        print("News already scraped today. Retrieving from cache...")
        print(cached_news)
        return

    url = "https://www.ambito.com/construccion-a5122808"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        news_items = soup.find_all('div', class_='article-content')
        news_content = ""
        for item in news_items:
            title = item.find('h2').get_text(strip=True)
            summary = item.find('p').get_text(strip=True)
            news_content += f"Title: {title}\nSummary: {summary}\n{'-' * 40}\n"
        print(news_content)
        save_news_to_db(today, news_content)

        with open(flag_file, 'w') as f:
            f.write(today)
    else:
        print("Failed to retrieve the news")

if __name__ == "__main__":
    scrape_news()
