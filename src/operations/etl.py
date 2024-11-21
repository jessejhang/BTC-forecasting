# src/operations/etl.py
import yfinance as yf
import pandas as pd
import json
import os
from src.database import Database

class DataFetcher:
    @staticmethod
    def get_bitcoin_price():
        btc_data = yf.Ticker("BTC-USD")
        current_price = btc_data.history(period="1d")['Close'][-1]
        return current_price

    @staticmethod
    def get_historical_data(symbol: str, period="1y"):
        data = yf.Ticker(symbol)
        history = data.history(period=period)
        return history[['Close']]

class ETLOperation:
    def __init__(self, db_handler: Database):
        self.db_handler = db_handler

    def extract_and_store(self, symbol="BTC-USD", period="1y"):
        # Extract data
        historical_data = DataFetcher.get_historical_data(symbol, period)
        
        # Store in database (or CSV/JSON as fallback)
        self.db_handler.store_data(historical_data, symbol)

    def run(self):
        # Example: Extract and store Bitcoin data
        self.extract_and_store(symbol="BTC-USD", period="1y")
