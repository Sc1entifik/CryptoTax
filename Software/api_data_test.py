import pytest
from datetime import datetime as dt
from time import sleep

from api_data import CoinGecko
from common_functions import dictionary_from_csv

"""
Run these tests with the -s flag due needing to interact with the coin choice menu when more than one coin gets returned from the coin_gecko_ticker_to_id.json file. The correct choice for the test is almost always the common sense choice. If you choose the wrong coin the test will fail and you will have to start over. If you are having trouble open up this file in your code editor and search for the terms in the to_49_names list. If the name is found that is the one you should choose from the menu.
"""
#A hard coded dictionary with the test_dates as keys, that returns a dictionary with the ticker symbols as keys, which returns a tuple of the expected price and the time in military hours the price in %H:%M:%S format from the coin gecko website.
@pytest.fixture
def date_ticker_price_time():
    return_dictionary = {
        "14-07-2018" : {"BNB":(11.91, "00:31:19"), "ETH":(449.96, "12:30:45"), "BTC":(6227.80, "11:30:59"), "LTC":(76.06, "04:31:35")},
        "21-09-2020" : {"BNB":(26.33, "02:16:49"), "ETH":(370.42, "04:07:30"), "BTC":(10964.26, "01:04:00"), "LTC":(47.29, "03:01:29")},
        "11-11-2022" : {"BNB":(298.42, "03:00:22"), "ETH":(1261.10, "11:00:53"), "BTC":(17423.23, "04:01:06"), "LTC":(63.07, "05:00:02")}
    }

    return return_dictionary

#Expected prices and times were manually gathered from the coin gecko website therefore may slightly diverge from what the coin gecko api returns thus a five percent tolerance is given.
def test_historic_price(date_ticker_price_time):
    five_percent_tolerance = lambda historic_price, expected_price: (abs(historic_price - expected_price) / expected_price) <= .05

    for date in date_ticker_price_time:
        for ticker in date_ticker_price_time.get(date):
            expected_price, time_on_date = date_ticker_price_time.get(date).get(ticker)
            date_time = f"{date} {time_on_date}"
            historic_price = CoinGecko(ticker, dt.strptime(date_time, "%d-%m-%Y %H:%M:%S")).return_historic_price()
            print(f"historic: {historic_price}\nexpected: {expected_price}\n\n")
            
            assert five_percent_tolerance(historic_price, expected_price) == True
    
#If API rate limit is reached you may get an empty coin_gecko_ticker_to_id.csv file due to the coin gecko api locking you out. If this is the case simply wait a 
def test_write_coin_gecko_json():
    cg_test_object = CoinGecko("BNB", dt.strptime("14-07-2018 00:31:19", "%d-%m-%Y %H:%M:%S"))
    cg_test_object.write_coin_gecko_json()
    top_49_tickers = ("BTC","ETH","USDT","BNB","XRP","USDC","STETH","ADA","DOGE","SOL","TRX","TON","DOT","MATIC","LTC","SHIB","DAI","BCH","LEO","AVAX","TUSD","UNI","LINK","XLM","BUSD","XMR","OKB","ETC","ATOM","HBAR","MNT","QNT","ICP","FIL","LDO","CRO","APT","ARB","VET","NEAR","OP","MKR","XDC","FRAX","AAVE","GRT","WBT","ALGO","KAS")
    top_49_names = ("bitcoin","ethereum","tether","binancecoin","ripple","usd-coin","staked-ether","cardano","dogecoin","solana","tron","the-open-network","polkadot","matic-network","litecoin","shiba-inu","dai","bitcoin-cash","leo-token","avalanche-2","true-usd","uniswap","chainlink","stellar","binance-usd","monero","okb","ethereum-classic","cosmos","hedera-hashgraph","mantle","quant-network","internet-computer","filecoin","lido-dao","crypto-com-chain","aptos","arbitrum","vechain","near","optimism","maker","xdce-crowd-sale","frax","aave","the-graph","whitebit","algorand","kaspa") 

    try:
        for ticker, name in zip(top_49_tickers, top_49_names):
            cg_test_object = CoinGecko(ticker, dt.strptime("14-07-2018 00:31:19", "%d-%m-%Y %H:%M:%S"))
            id_from_ticker = cg_test_object._get_coin_id_from_ticker()
            print(f"\nticker: {ticker}\nname: {name}\n")
            assert id_from_ticker == name

    except AttributeError:
        print("You have likely reached the Coin Gecko API limit. We bill try recalling the function again in a little over a minute. If this message has repeated more than two times please STOP with ctrl-c so you don't get locked out from using the Coin Gecko API. In that case give it 5-10 more minutes before trying again.")
        sleep(72)

        return test_write_coin_gecko_json()

