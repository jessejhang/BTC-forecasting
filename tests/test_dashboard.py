# modules/data_fetcher.py
import yfinance as yf

class DataFetcher:
    @staticmethod
    def get_bitcoin_price():
        btc_data = yf.Ticker("BTC-USD")
        current_price = btc_data.history(period="1d")['Close'][-1]
        return current_price

    @staticmethod
    def get_historical_bitcoin_data():
        btc_data = yf.Ticker("BTC-USD")
        history = btc_data.history(period="1y")  # 1 year of data
        return history[['Close']]
