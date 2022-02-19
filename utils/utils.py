import datetime
import json
import time
import requests


# Today's unix time
def today():
    return time.mktime(datetime.date.today().timetuple())


# Yesterday's unix time
def yesterday():
    return time.mktime((datetime.date.today() - datetime.timedelta(days=1)).timetuple())


# Amount with the right decimals
def get_amount(amount, decimals):
    return float(amount) / 10**decimals


# Current price query
def get_current_price(from_sym, to_sym):
    url = 'https://min-api.cryptocompare.com/data/price'
    parameters = {'fsym': from_sym, 'tsyms': to_sym}
    response = requests.get(url, params=parameters)
    data = response.json()
    return data


# API query handling
def query_api(path: str, data: {}, header: {}):
    try:
        response = requests.post(path, json=data, headers=header)
        if response and response.ok:
            data = json.loads(response.text)
        else:
            print('Error retrieving data for {}:  {}'.format(path, response.text))
            data = {}
        return data
    except:
        print('Error retrieving data for {}: Unable to connect to API'.format(path))


#  Common entry result
def create_entry(chain: str, ticker: str, today_coins: float, yesterday_coins: float, price: float):
    return {
        'chain': chain,
        'ticker': ticker,
        'today_coins': "{:.4f}".format(today_coins),
        'today_value': "{:.2f}".format(today_coins * price),
        'yesterday_coins': "{:.4f}".format(yesterday_coins),
        'yesterday_value': "{:.2f}".format(yesterday_coins * price)
    }
