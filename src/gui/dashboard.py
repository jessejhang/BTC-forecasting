# src/dashboard.py
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from src.operations.visualize import VisualizeOperation
from src.forecasting.model_manager import ModelManager
from src.operations.etl import ETLOperation
from src.database import Database
import numpy as np
import sys

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Bitcoin Forecast Dashboard')
        self.setGeometry(100, 100, 800, 600)
        
        # Initialize components
        self.layout = QVBoxLayout(self)
        self.info_label = QLabel('Bitcoin Price: $0', self)
        self.layout.addWidget(self.info_label)
        
        self.visualize_operation = VisualizeOperation(self)  # Visualize operation
        self.layout.addWidget(self.visualize_operation)  # Add visualize to layout
        
        self.start_button = QPushButton("RUN Regular Operation", self)
        self.start_button.clicked.connect(self.run_regular_operation)
        self.layout.addWidget(self.start_button)

        self.manual_button = QPushButton("RUN Manual Operation", self)
        self.manual_button.clicked.connect(self.run_manual_operation)
        self.layout.addWidget(self.manual_button)

        # Initialize models and operations
        self.db_handler = Database()  # Database handler
        self.operation = ETLOperation(self.db_handler)  # ETL operation
        self.model_manager = ModelManager()  # Model manager

        # Timer to update Bitcoin price every 30 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_bitcoin_price)
        self.timer.start(30000)  # 30 seconds interval

        self.show()

    def update_bitcoin_price(self):
        # Get the latest Bitcoin price and update the label
        price = self.operation.get_bitcoin_price()
        self.info_label.setText(f'Bitcoin Price: ${price:.2f}')

    def run_regular_operation(self):
        # Run ETL operation every 15 minutes and perform forecasting
        self.operation.extract_and_store(symbol="BTC-USD", period="1y")  # Example: Run ETL for 1 year of Bitcoin data
        historical_data = self.db_handler.fetch_data(table_name="bitcoin_data")["Close"].values
        forecast_data = self.model_manager.forecast(historical_data)
        
        # Visualize the data
        self.visualize_operation.plot_bitcoin_data(historical_data, forecast_data)

    def run_manual_operation(self):
        # Manual operation example (e.g., running a specific operation on demand)
        self.operation.extract_and_store(symbol="BTC-USD", period="1y")
        historical_data = self.db_handler.fetch_data(table_name="bitcoin_data")["Close"].values
        forecast_data = self.model_manager.forecast(historical_data)
        
        # Visualize the data
        self.visualize_operation.plot_bitcoin_data(historical_data, forecast_data)
