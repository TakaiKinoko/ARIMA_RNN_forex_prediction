import datetime
import requests
from collections import defaultdict
import pandas as pd
import requests
from requests.exceptions import HTTPError

OUT_PATH = "forex_16-17_1.csv"
API_KEY = "ba8420e66e5149808b598c9508b6de81" # MY APP ID

def format_url(date):
    return f'https://openexchangerates.org/api/historical/{date}.json?app_id={API_KEY}'

def get_requst(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}') 
    except Exception as err:
        print(f'Other error occurred: {err}') 
        raise
    else:
        return response.json()

def run():
    dates_forex = {'Date': [], 'EUR': [], 'JPY': [], 'GBP': [], 'CNY': []}

    s, e = datetime.date(2016,1,1), datetime.date(2017,7,8)
    diff = e - s

    for i in range(diff.days + 1):
        curr_date = s + datetime.timedelta(i)
        dates_forex['Date'].append(curr_date)
        print(f"Downloading {curr_date} ...")

        url = format_url(curr_date)
        res = get_requst(url)
        for name, rate in res['rates'].items():
            _rates = {}
            if name in {"EUR", "JPY", "GBP", "CNY"}:
                dates_forex[name].append(rate)

    print("Now generating csv file...")
    df = pd.DataFrame(data=dates_forex)
    df = df.set_index('Date')
    df = df.sort_values(by=['Date'])
    df.to_csv(OUT_PATH)
    print(f"Data saved in {OUT_PATH} successfully!")

if __name__ == "__main__":
    run()
