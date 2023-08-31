import os
import requests
import sqlite3
from time import time, sleep
import logging

from face_request import Face_Unlim


API = Face_Unlim(cookie_token="")
API_token = API.get_token("Roberta")
API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
err_count = 0

def query(payload):
    return requests.post(API_URL, headers={"Authorization": f"Bearer {API_token}"}, json={"inputs": payload}).json()


def split_text(inp_text: str, num=2000):
    res = []
    text_list = inp_text.split(' ', -1)
    text_length = len(inp_text)
    if text_length > num:
        for _ in range(text_length // num + 1):
            curr_str = ''
            while len(curr_str) < (text_length // (text_length // num + 1)) and text_list:
                curr_str += f'{text_list.pop(0)} '
            res.append(curr_str)
        return res
    else:
        return [inp_text]


logging.basicConfig(filename='errors.log', level=logging.ERROR)
start_time = time()
average_time = [0]
max_text_len = 1000
order = ['neutral', 'negative', 'positive']

# Get the directory
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "..", "news.db")

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS news_rating_roberta
                      (data_id INTEGER PRIMARY KEY,
                        title_neutral REAL,
                        title_negative REAL,
                        title_positive REAL,
                        text_neutral REAL,
                        text_negative REAL,
                        text_positive REAL);''')

    cursor.execute('''SELECT nc.data_id, nc.title, nc.text
        FROM news_content AS nc LEFT JOIN news_rating_roberta ON nc.data_id = news_rating_roberta.data_id
        WHERE news_rating_roberta.title_negative IS NULL OR news_rating_roberta.text_negative IS NULL''')

    for (data_id, title, text) in cursor.fetchall():
        try:
            query_list = [title]
            query_list.extend(split_text(text, max_text_len))
            response = query(query_list)
            print('-->', data_id)
            print(response)
            title_score = [round(score['score'], 5) for label in order for score in response[0] if score['label'] == label]
            if len(text) > max_text_len:
                text_score_list = []
                for i in response[1:]:
                    text_score_list.append([round(score['score'], 5) for label in order for score in i if
                                   score['label'] == label])
                    print(text_score_list[-1])
                text_score = [round(sum(col)/len(col), 5) for col in zip(*text_score_list)]
            else:
                text_score = [round(score['score'], 5) for label in order for score in response[1] if
                                   score['label'] == label]
            print('-----', title_score)
            print('-----', text_score)
            print(round((time() - start_time), 4), '|   ', sum(average_time)/len(average_time))
            cursor.execute('''INSERT OR REPLACE INTO news_rating_roberta
                                                 (data_id, title_neutral, title_negative, title_positive,
                                                            text_neutral, text_negative, text_positive)
                                                 VALUES (?, ?, ?, ?, ?, ?, ?);''',
                           (data_id, title_score[0], title_score[1], title_score[2], text_score[0], text_score[1], text_score[2]))
            conn.commit()
            err_count = 0
        except Exception as e:
            if "currently loading" in response['error']:
                sleep(int(response["estimated_time"]))
            elif "Please subscribe to a plan" in response['error']:
                API_token = API.update_token("Roberta")
                sleep(5)
            elif "Service Unavailable" in response['error']:
                sleep(30)
            elif err_count > 100:
                quit()
            else:
                err_count += 1
            print('ERROR!')
            logging.error(f"{response} - {int(time())}: {data_id} {title}")
        average_time.append(round((time() - start_time), 2))
        start_time = time()