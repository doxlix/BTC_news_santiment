import requests
import sqlite3
from bs4 import BeautifulSoup

DATABASE_FILE = "news.db"
BASE_URL = "https://cryptonews.net/news/bitcoin/"


def scrape_news_content(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, features="html.parser")

    reading_time_elem = soup.find("div", "flex middle-xs reading-time")
    reading_time = int(reading_time_elem.text.strip().split("~")[-1].split(" ")[0]) if reading_time_elem else None

    title_elem = soup.find("h1", "article_title")
    title = title_elem.text.strip() if title_elem else None

    text_elems = soup.find("div", "news-item detail content_text").find_all("p")
    text = '\n'.join(paragraph.text.strip() for paragraph in text_elems) if text_elems else None

    return reading_time, title, text


def update_news_content_table(conn, data_id, reading_time, title, text):
    with conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT OR REPLACE INTO news_content 
                          (data_id, reading_time, title, text) 
                          VALUES (?, ?, ?, ?);''', (data_id, reading_time, title, text))


def scrape_and_store_news_content():
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS news_content 
                          (data_id INTEGER PRIMARY KEY, 
                           reading_time INTEGER, 
                           title TEXT, 
                           text TEXT);''')

        cursor.execute('''SELECT news.data_id 
                        FROM news 
                        LEFT JOIN news_content ON news.data_id = news_content.data_id 
                        WHERE news_content.data_id IS NULL 
                        ORDER BY news.data_id DESC;''')
        data_ids = [row[0] for row in cursor.fetchall()]

        batch_size = 50
        for req_count, data_id in enumerate(data_ids, start=1):
            url = f"{BASE_URL}/{data_id}/"
            reading_time, title, text = scrape_news_content(url)
            update_news_content_table(conn, data_id, reading_time, title, text)

            print(f"{data_id} - {title}")

            if req_count % batch_size == 0:
                conn.commit()

        conn.commit()
