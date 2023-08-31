import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import sqlite3
import re


with sqlite3.connect(r"C:\Users\lazzz\PycharmProjects\News_Parse\news.db") as conn:
    cursor = conn.cursor()

    w_count = {}
    cursor.execute('''SELECT title
    FROM news''')
    titles = cursor.fetchall()
    for title in titles:
        title = title[0].split(maxsplit=-1)
        for word in title:
            word = re.sub(r'[^\w\s]', '', word.strip().lower())
            if len(word) > 2:
                if word[-1] == 's':
                    word = word[:-1]
            if word in w_count:
                w_count[word] += 1
            else:
                w_count[word] = 1

    sorted_dict = dict(sorted(w_count.items(), key=lambda item: item[1], reverse=True))
    sorted_dict = {i: sorted_dict[i] for i in sorted_dict if sorted_dict[i] > 100}
    h = ['price', 'crypto', 'market', 'analyst', 'analysi', 'bull', 'high', 'new', 'hit', 'above',
     'below', 'trader', 'support', 'rally', 'bullish', 'level', 'drop', 'next', 'over', 'us', 'top',
     'bear', 'break', 'whale', 'resistance', 'low', 'key', 'buy', 'investor', 'bottom',
     'hold', 'ceo', 'million', 'back', 'onchain', 'dip', 'etf', 'move', 'gold',
     'first', 'crash', 'network', 'signal', 'continue', 'surge', 'near',
     'fall', 'future', 'predict', 'bearish', 'rate', 'target', 'indicator', 'despite', 'close',
     'stock', 'lightning', 'technical', 'peter', 'prediction', 'exchange', 'run', 'salvador', 'reason', 'trading',
     'rise', 'remain', 'report', 'miner', 'correction', 'record', 'breakout', 'asset', 'bank', 'fed', 'billion',
     'volatility', 'gain', 'risk', 'ethereum', 'major', 'higher', 'bounce', 'dollar', 'last', 'trend',
     'end', 'massive', 'set', 'reach', 'soon', 'supply', 'worth', 'pattern', 'adoption', 'short', 'inflation',
     'option', 'transaction', 'big', 'halving', 'fund', 'metric', 'expect', 'payment', 'long', 'likely', 'buying',
     'holder', 'watch', 'past', 'value', 'volume', 'sign', 'eye', 'mining', 'wallet', 'under', 'look', 'cap',
     'holding', 'claim', 'warn', 'interest', 'strong', 'schiff', 'plunge', 'microstrategy', 'face', 'chart',
     'toward', 'altcoin', 'following', 'fear', 'dominance', 'point', 'mean', 'explain', 'crucial', 'selling', 'spike',
     'selloff', 'decline', 'money', 'shortterm', 'start', 'fresh', 'bloomberg', 'sell', 'recent', 'turn',
     'lower', 'coming', 'trade', 'expert', 'musk', 'longterm', 'addresse', 'call', 'struggle', 'recovery',
     'further', 'return', 'macro', 'increase', 'march', 'elon', 'momentum', 'possible',
     'global', 'investment', 'strategist', 'cycle', 'twitter', 'reclaim', 'tesla', 'world', 'mark', 'upside',
     'rebound', 'reveal', 'fail', 'critical', 'ath', 'china', 'digital', 'sentiment', 'retest', 'breaking',
     'accumulation', 'mike', 'incoming', 'good', 'potential', 'institutional', 'reserve', 'against', 'grayscale', 'firm', 'forecast', 'saylor', 'brandt', 'losse', 'collapse', 'veteran', 'test', 'michael', 'open', 'billionaire', 'reversal', 'binance', 'sec', 'outlook', 'lose', 'imminent']

    res = {}
    for i in h:
        res[i] = sorted_dict[i]
    print(res)