import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from common_functions import dictionary_from_csv
import json
import csv
from datetime import datetime
from time import sleep

class CoinGecko():
    coin_gecko_ticker_id_filepath = '../CSV/API/coin_gecko_ticker_to_id.csv'
    requests_url = 'https://api.coingecko.com/api/v3/coins/'
    coin_list_endpoint = 'list?include_platform=false'

    def __init__(self, ticker_symbol, historical_dt):
        self.ticker = ticker_symbol.lower()
        self.query_date = historical_dt.strftime('%d-%m-%Y')
        #needed to keep writing unwanted ticker, id dictionary pairs to coin_gecko_ticker_to_id.csv
        self.unwanted_coin_gecko_ids = ['ethereum-wormhole', 'thorchain-erc20', 'oec-binance-coin', 'heco-peg-bnb', 'binance-coin-wormhole']

    
    #needed to convert ticker symbols to id parameters which Coin Gecko uses to pull data
    def write_ticker_to_id_csv(self):

        with requests.Session() as coin_list:
            coin_list_object = coin_list.get(f'{CoinGecko.requests_url}{CoinGecko.coin_list_endpoint}')
            coin_list_object.content.decode('utf-8')
            coin_list_json = coin_list_object.json()

        with open(CoinGecko.coin_gecko_ticker_id_filepath, 'w') as ticker_to_id:
            csv_object = csv.writer(ticker_to_id)
            header = ['key','value']
            csv_object.writerow(header)

            for coin in coin_list_json:
                if coin.get('id') not in self.unwanted_coin_gecko_ids:
                    csv_object.writerow([coin.get('symbol'), coin.get('id')])

        return f'Ticker to ID conversion file written to {CoinGecko.coin_gecko_ticker_id_filepath}!'


    def return_historical_price(self):
        ticker_to_id = dictionary_from_csv(CoinGecko.coin_gecko_ticker_id_filepath)
        price_query_url = f'{CoinGecko.requests_url}{ticker_to_id.get(self.ticker)}/history?date={self.query_date}&localization=false'

        with requests.Session() as historical_price:
            try:
                historical_price_object = historical_price.get(price_query_url)
                historical_price_object.content.decode('utf-8')
                historical_price_json = historical_price_object.json()

            except ConnectionError:
                print('Your historical price query failed due to a Connection Error. We will try to call the function again in one minute. If this creates an endless loop break with ctrl-c')
                sleep(62)
                return self.return_historical_price()

            except TimeoutError:
                print('A timeout error occured.')

            except TooManyRedirects:
                print('Your query failed do to too many redirects.')

        try:
            return historical_price_json.get('market_data').get('current_price').get('usd')

        except AttributeError:
            print(f'Your query failed because historical_price_json is a NoneType object\n\nticker: {self.ticker}\nlookup_date: {self.query_date}\nticker_id: {ticker_to_id.get(self.ticker)}')
            print('\n\nThis attribute error may have occured do to reaching API limits. We will try to call the function again in one minute. Give this loop at least two iterations before giving up by pressing ctrl-c. \n\nIf the same loop values have been stuck for more than two iterations you can add the ticker_id value shown above to self.unwanted_coin_gecko_ids in the __init__() function of the CoinGecko class of the api_data.py file in the Software folder.\n')
            sleep(72)
            return self.return_historical_price()

'''
cg = CoinGecko('BNB', datetime.strptime('03-27-2022','%m-%d-%Y'))
print(cg.write_ticker_to_id_csv())
'''
