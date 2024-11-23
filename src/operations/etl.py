import yfinance as yf
import pandas as pd
import sys, os, time
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

class DataFetcher:
    @staticmethod
    def get_bitcoin_price():
        """
        Fetch real-time Bitcoin price using yfinance.
        """
        btc_data = yf.Ticker("BTC-USD")
        current_price = btc_data.history(period="1d")['Close'].iloc[-1]
        return current_price

    @staticmethod
    def get_historical_data(symbol: str, period="1y"):
        """
        Fetch historical data for a given symbol and time period.
        """
        data = yf.Ticker(symbol)
        history = data.history(period=period)
        history.reset_index(inplace=True)
        return history[['Date', 'Close']]

class ETLOperation:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def save_initial_data(self):
        """
        Save historical Bitcoin data to CSV.
        """
        data = DataFetcher.get_historical_data("BTC-USD", period="1y")
        data.to_csv(self.csv_path, index=False)
        print(f"Initial data saved to {self.csv_path}")

    def track_price(self):
        """
        Continuously track price changes and update the CSV file.
        """
        last_price = None

        while True:
            try:
                # Fetch the current price
                current_price = DataFetcher.get_bitcoin_price()
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Append to CSV if the price changes
                if last_price is None or current_price != last_price:
                    new_row = pd.DataFrame([[current_time, current_price]], columns=["Date", "Close"])
                    new_row.to_csv(self.csv_path, mode='a', header=False, index=False)
                    print(f"Price updated: {current_time}: ${current_price:.2f}")
                    last_price = current_price

                time.sleep(5)

            except Exception as e:
                print(f"Error: {e}")
                break

if __name__ == "__main__":
    csv_file_path = os.path.join("data", "bitcoin_data_2024.csv")
    os.makedirs("data", exist_ok=True)  # Ensure the directory exists

    etl = ETLOperation(csv_path=csv_file_path)
    etl.save_initial_data()  # Save the initial data
    etl.track_price()        # Start tracking price changes
