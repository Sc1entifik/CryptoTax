import pytest
from datetime import datetime as dt

from api_data import CoinGecko

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
    

    
    
    
