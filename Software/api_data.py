import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from datetime import datetime
from time import sleep

class CoinGecko():
    coin_gecko_ticker_id_filepath = "../CSV/API/coin_gecko_ticker_to_id.json"
    requests_url = "https://api.coingecko.com/api/v3/coins/"
    coin_list_endpoint = "list?include_platform=false"
    unwanted_search_terms = ("-wormhole", "-binance-", "-peg-", "-pulsechain", "pulsecchain-", "bridged-", "-bridge", "wrapped-")

    def __init__(self, ticker_symbol, historic_dt):
        self.ticker = ticker_symbol.lower()
        self.query_date = historic_dt.strftime('%d-%m-%Y %H:%M:%S')


    def _load_coin_gecko_json(self):
        with open(CoinGecko.coin_gecko_ticker_id_filepath) as coin_gecko_object:
            cg_json = json.load(coin_gecko_object)

        return cg_json


    def _get_coin_id_from_ticker(self):
        coin_gecko_json = self._load_coin_gecko_json()
        found_coins = [coin for coin in coin_gecko_json if coin.get("symbol") == self.ticker and True not in map(lambda x: False if coin.get("id").find(x) == -1 else True, CoinGecko.unwanted_search_terms)]

        if len(found_coins) == 1:
            return found_coins[0].get("id")

        elif len(found_coins) == 0:
            return "Sorry your coin wasn't found in the Coin Gecko API. The filter was probably too strict."

        else:
            found_coin_dict = {str(i+1): found_coins[i] for i in range(len(found_coins))}
            print("More than one coin found. Please choose the coin you traded from the following list\n")

            for index, coin in found_coin_dict.items():
                print(f"{index}) {coin}")

            coin_choice = None
            print()

            while not coin_choice:
                coin_choice = found_coin_dict.get(input("Please enter one of the coin numbers listed above\n"))

            return coin_choice.get("id")

    
    #needed to convert ticker symbols to id parameters which Coin Gecko uses to pull data
    def write_coin_gecko_json(self):

        with requests.Session() as requests_object:
            coin_json = json.loads(requests_object.get(f"{CoinGecko.requests_url}{CoinGecko.coin_list_endpoint}").content.decode("utf-8"))

        with open(CoinGecko.coin_gecko_ticker_id_filepath, "w") as json_file:
            json.dump(coin_json, json_file)

        return f"API file has been written to {CoinGecko.coin_gecko_ticker_id_filepath}!"


    def return_historic_price(self):
        price_query_url = f"{CoinGecko.requests_url}{self._get_coin_id_from_ticker()}/history?date={self.query_date}&localization=false"

        with requests.Session() as requests_object:
            try:
                historic_price_json = json.loads(requests_object.get(price_query_url).content.decode("utf-8"))

            except ConnectionError:
                print("Your historic price query failed due to a Connection Error. We will try to call the function again in one minute. If this creates an endless loop break with ctrl-c")
                sleep(62)
                return self.return_historic_price()

            except TimeoutError:
                print("A timeout error occured.")

            except TooManyRedirects:
                print("Your query failed do to too many redirects.")

        try:
            return historic_price_json.get("market_data").get("current_price").get("usd")

        except AttributeError:
            print(f"Your query failed because historic_price_json is a NoneType object\n\nticker: {self.ticker}\nlookup_date: {self.query_date}\nticker_id: {self._get_coin_id_from_ticker()}")
            print("\n\nThis attribute error likely occured do to reaching API limits. We will try to call the function again in one minute. Give this loop at least two iterations before giving up by pressing ctrl-c. \n\nIf the same loop values have been stuck for more than two iterations check to make sure your internet connection is intact. Assuming your internet connection is good it is possible that Coin Gecko doesn't have the historic data either for that coin or for that coin for that date. Go to Coin Gecko.com and look up the coin you are looking for and see if the date goes back as far as the date you are trying to look up.\n")
            sleep(72)
            return self.return_historic_price()
