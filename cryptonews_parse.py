import requests
import sqlite3
from bs4 import BeautifulSoup


URL = "https://cryptonews.net/en/api/article/list/"
HEADERS = {'Content-Type': 'application/json'}


def scrape_and_store_articles():
    # Initialize database connection and cursor
    with sqlite3.connect('news.db') as conn:
        cur = conn.cursor()

        # Create news table if it doesn't exist
        cur.execute('''CREATE TABLE IF NOT EXISTS news
                       (data_id INTEGER PRIMARY KEY,
                        title TEXT,
                        domain TEXT,
                        link TEXT,
                        datetime TEXT,
                        color TEXT,
                        mark TEXT,
                        image TEXT)''')
        page = 3
        while True:
            query_payload = {"page": page, "query_list": "", "rubric": "bitcoin"}
            resp = requests.post(URL, json=query_payload, headers=HEADERS)
            articles_html = resp.json()['html']

            if not articles_html:
                break

            soup = BeautifulSoup(articles_html, features="html.parser")
            elements = soup.find_all("div", "row news-item start-xs")

            for element in elements:
                data_id = element["btc_data-id"].split("/")[-2]
                image = element["btc_data-image"]
                domain = element["btc_data-domain"]
                link = element["btc_data-link"]
                title = element["btc_data-title"]
                mark = element.find("span", "mark").text
                color = element.find("div", "rating-color")["style"].split("#")[-1] if element.find("div",
                                                                                                    "rating-color") else None
                data_datetime = element.find("span", "datetime").text.strip()

                # Insert data into the database
                cur.execute('''INSERT OR REPLACE INTO news VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                            (data_id, title, domain, link, data_datetime, color, mark, image))
                print(data_id, title)

            page += 1
            conn.commit()