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


def three_plots_for_dataset(dates_time, neutral, negative, positive, text_or_title=False):
    dates = [datetime.strptime(d, '%d %B %Y %H:%M, UTC') for d in dates_time]
    dates = [i.date() for i in dates]
    dates.sort()
    dates_count = {i:dates.count(i) for i in set(dates)}
    rating = [round(i, 3) for i in neutral + negative + positive]
    rating.sort()
    rating_count = {i:rating.count(i) for i in set(rating)}

    fig = plt.figure()
    ax1 = plt.subplot2grid((3, 5), (0, 0), colspan=4)
    ax2 = plt.subplot2grid((3, 5), (1, 0), colspan=4, rowspan=2)
    ax3 = plt.subplot2grid((3, 5), (1, 4), rowspan=2)

    ax1.bar(dates_count.keys(), dates_count.values(), width=1, color='black')
    ax2.scatter(dates, neutral, color='black', marker='*', s=0.01)
    ax2.scatter(dates, positive, color='black', marker='*', s=0.01)
    ax2.scatter(dates, negative, color='black', marker='*', s=0.01)
    ax3.barh(list(rating_count.keys()), list(rating_count.values()), height=0.001, color='black')

    fig.subplots_adjust(hspace=0, wspace=0, left=0.05, right=0.99, top=0.97, bottom=0.07)
    ax1.set_xticks([])

    ax1.set_title('Articles per day', fontsize=10)
    ax1.set_xlim(mdates.date2num(dates[0]), mdates.date2num(dates[-1])+10)

    ax2.set_xlabel('Date', fontsize=10)
    if text_or_title:
        ax2.set_ylabel('Article title rating (0: 1)\n(neutral, negative, positive)', fontsize=10)
    else:
        ax2.set_ylabel('Article rating (0: 1)\n(neutral, negative, positive)', fontsize=10)
    ax2.set_xlim(mdates.date2num(dates[0]), mdates.date2num(dates[-1])+10)
    ax2.set_ylim(0, 1)

    ax3.set_xlabel('Rating distribution', fontsize=10)
    ax3.set_yticks([])
    ax3.set_ylim(0, 1)

    plt.show()
with sqlite3.connect(r"C:\Users\lazzz\PycharmProjects\News_Parse\news.db") as conn:
    cursor = conn.cursor()
    # dates_time, title_neutral, title_negative, title_positive, text_neutral, text_negative, text_positive = zip(*cursor.fetchall())
    # days_of_week = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0, 'Sunday': 0}
    # dates = [datetime.strptime(d, '%d %B %Y %H:%M, UTC') for d in dates_time]
    # dates = [page.date() for page in dates]
    # dates.sort()
    # dates_count = {page: dates.count(page) for page in set(dates)}
    # dates_sum = {page: [0, 0, 0] for page in set(dates)}
    # for date, neutral, negative, positive in zip(dates, text_neutral, text_negative, text_positive):
    #     dates_sum[date] = [page+j for page, j in zip([neutral, negative, positive], dates_sum[date])]
    # dates_avg = {page: [round(j/dates_count[page], 5) for j in dates_sum[page]] for page in set(dates)}
    # plt.scatter(dates_avg.keys(), [page[0] for page in dates_avg.values()])
    # plt.scatter(dates_avg.keys(), [page[1] for page in dates_avg.values()], color='blue')
    # plt.scatter(dates_avg.keys(), [page[2] for page in dates_avg.values()], color='red')
    #
    # plt.show()


    cursor.execute('''SELECT
       n.datetime,
       nrf.title_neutral,
       nrf.title_negative,
       nrf.title_positive,
       nrf.text_neutral,
       nrf.text_negative,
       nrf.text_positive
       FROM news_rating_roberta nrf INNER JOIN news n ON nrf.data_id = n.data_id
       ORDER BY n.data_id;''')

    get_data = np.array(cursor.fetchall())
    date_btc, price, op, hi, lo, vol, delt = np.genfromtxt(r'C:\Users\lazzz\PycharmProjects\News_Parse\Bitcoin Historical Data - Week.csv',
                                                           delimiter=';', skip_header=1, dtype=None, encoding='utf-8',
                                                           converters={0: lambda x: datetime.strptime(x, '%b %d %Y'),
                                                                       1: lambda x: float(x.replace(',', '', -1)), 2: lambda x: float(x.replace(',', '', -1)),
                                                                       3: lambda x: float(x.replace(',', '', -1)), 4: lambda x: float(x.replace(',', '', -1)),
                                                                       6: lambda x: float(x[:-1])}, unpack=True)


    dates = list(map(lambda date_str: parse_date(date_str, 'w'), get_data[:, 0]))
    daily_values = {}
    for i in range(len(get_data)):
        date = dates[i]
        if date not in daily_values:
            daily_values[date] = []
        daily_values[date].append(get_data[i, 1:].astype(float))
    daily_averages = {date: np.mean(np.array(values), axis=0) for date, values in daily_values.items()}

    # ax1 = plt.subplot2grid((2, 3), (0, 0), colspan=3)
    # ax2 = plt.subplot2grid((2, 3), (1, 0), colspan=3)


    # plt.plot(date_btc, [page/max(price) for page in price], daily_averages.keys(), [page[5] for page in daily_averages.values()])

    # plt.semilogy() #log y
    # plt.show()

    # plt.plot(daily_averages.keys(), [page[3] for page in daily_averages.values()], color='black')
    # plt.plot(daily_averages.keys(), [page[4] for page in daily_averages.values()], color='blue')
    # plt.plot(daily_averages.keys(), [page[5] for page in daily_averages.values()], color='red')
    # plt.title('Weekly averaged sentiment rating (roberta)')
    # plt.fill_between(daily_averages.keys(), [page[4] for page in daily_averages.values()], where=[j - k >= 0 for j, k in zip([page[5] for page in daily_averages.values()], [page[4] for page in daily_averages.values()])], interpolate=True, facecolor='green')
    # plt.fill_between(daily_averages.keys(), [page[4] for page in daily_averages.values()], where=[k - j >= 0 for j, k in zip([page[5] for page in daily_averages.values()], [page[4] for page in daily_averages.values()])], interpolate=True,facecolor='red')

    indicator = [(p - n) * (1 - t) for t, n, p in zip([i[3] for i in daily_averages.values()], [i[4] for i in daily_averages.values()], [i[5] for i in daily_averages.values()])]

    # fig, ax1 = plt.subplots()
    # ax1.grid(True, which='both')
    # ax1.plot(date_btc, price, color='black', linewidth=2)
    # ax2 = ax1.twinx()
    # ax2.plot(daily_averages.keys(), indicator, color='black', linewidth=1)
    # ax2.axhline(0, color='black')
    # ax2.fill_between(daily_averages.keys(), indicator, 0, where=[page > 0 for page in indicator], facecolor='#32A852', interpolate=True)
    # ax2.fill_between(daily_averages.keys(), indicator, 0, where=[page < 0 for page in indicator], facecolor='#b03138', interpolate=True)
    # ax1.set_ylim(-18000, 68000)
    # ax2.set_ylim(-0.235, 1.5)
    # ax1.set_yticks([])
    # ax2.set_yticks([])
    plt.tight_layout()
    # plt.title('BTC price and sentiment indicator')
    plt.show()