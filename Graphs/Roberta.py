import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import sqlite3
import numpy as np

def parse_date(date_str, max_date=''):
    if not max_date:
        return datetime.strptime(date_str, '%d %B %Y %H:%M, UTC')
    if max_date == 'd':
        dt = datetime.strptime(date_str, '%d %B %Y %H:%M, UTC')
        return datetime.strptime(dt.strftime('%Y-%m-%d'), '%Y-%m-%d')
    if max_date == 'w':
        dt = datetime.strptime(date_str, '%d %B %Y %H:%M, UTC')
        start_of_week = dt - timedelta(days=dt.weekday())
        return datetime.strptime(start_of_week.strftime('%Y-%m-%d'), '%Y-%m-%d')
    if max_date == 'm':
        dt = datetime.strptime(date_str, '%d %B %Y %H:%M, UTC')
        return datetime.strptime(dt.strftime('%Y-%m'), '%Y-%m')
    if max_date == 'y':
        dt = datetime.strptime(date_str, '%d %B %Y %H:%M, UTC')
        return datetime.strptime(dt.strftime('%Y'), '%Y')


with sqlite3.connect(r"C:\Users\lazzz\PycharmProjects\News_Parse\news.db") as conn:
    cursor = conn.cursor()

    cursor.execute('''SELECT
       n.datetime,
       nrf.title_neutral,
       nrf.title_negative,
       nrf.title_positive,
       nrf.text_neutral,
       nrf.text_negative,
       nrf.text_positive
       FROM news_rating_finbert nrf INNER JOIN news n ON nrf.data_id = n.data_id
       ORDER BY n.data_id;''')

    date_time,  neutral, negative, positive, _, _, _ = zip(*cursor.fetchall())


    dates = [datetime.strptime(d, '%d %B %Y %H:%M, UTC') for d in date_time]
    rating_neutral = [round(i, 3) for i in neutral]
    rating_negative = [round(i, 3) for i in negative]
    rating_positive = [round(i, 3) for i in positive]
    rating_count_1 = {i: rating_neutral.count(i) for i in set(rating_neutral)}
    rating_count_2 = {i: rating_negative.count(i) for i in set(rating_negative)}
    rating_count_3 = {i: rating_positive.count(i) for i in set(rating_positive)}

    fig = plt.figure()
    ax1 = plt.subplot2grid((3, 5), (0, 0), colspan=4)
    ax2 = plt.subplot2grid((3, 5), (1, 0), colspan=4)
    ax3 = plt.subplot2grid((3, 5), (2, 0), colspan=4)
    ax4 = plt.subplot2grid((3, 5), (0, 4))
    ax5 = plt.subplot2grid((3, 5), (1, 4))
    ax6 = plt.subplot2grid((3, 5), (2, 4))

    ax1.scatter(dates, neutral, color='black', marker='*', s=0.01)
    ax2.scatter(dates, negative, color='blue', marker='*', s=0.01)
    ax3.scatter(dates, positive, color='red', marker='*', s=0.01)
    ax4.barh(list(rating_count_1.keys()), list(rating_count_1.values()), height=0.001, color='black')
    ax5.barh(list(rating_count_2.keys()), list(rating_count_2.values()), height=0.001, color='blue')
    ax6.barh(list(rating_count_3.keys()), list(rating_count_3.values()), height=0.001, color='red')

    fig.subplots_adjust(hspace=0, wspace=0, left=0.05, right=0.99, top=0.97, bottom=0.07)

    for i in (ax1, ax2, ax3):
        i.set_xlim(mdates.date2num(dates[0]), mdates.date2num(dates[-1]) + 10)
        i.set_xticks([])
        i.set_yticks([])
        i.set_ylim(0, 1)
    for i in (ax4, ax5, ax6):
        i.set_ylim(0, 1)
        i.set_xticks([])
        i.set_yticks([])

    print(max(neutral), max(negative), max(positive))

    plt.show()