# src/operations/visualize.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
import numpy as np

class VisualizeOperation(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Visualize Forecast and Data")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout(self)
        self.info_label = QLabel('Visualizing Bitcoin Data and Forecasts', self)
        self.layout.addWidget(self.info_label)

        self.canvas = FigureCanvas(plt.figure())
        self.layout.addWidget(self.canvas)

        self.plot_button = QPushButton("Plot Bitcoin Data and Forecast", self)
        self.plot_button.clicked.connect(self.plot_bitcoin_data)
        self.layout.addWidget(self.plot_button)

        self.show()

    def plot_bitcoin_data(self, historical_data, forecast_data):
        """Plots both historical data and forecasted data on a graph"""
        # Clear the canvas before plotting
        self.canvas.figure.clf()
        ax = self.canvas.figure.add_subplot(111)

        # Plot the historical data as a line
        ax.plot(historical_data, label="Historical Bitcoin Data", color='blue', linestyle='-', marker='o')

        # Plot the forecasted data as a line with dots
        ax.plot(range(len(historical_data), len(historical_data) + len(forecast_data)),
                forecast_data, label="Forecasted Bitcoin Data", color='red', linestyle='-', marker='x')

        # Adding titles and labels
        ax.set_title("Bitcoin Price Data & Forecast")
        ax.set_xlabel("Time (Days)")
        ax.set_ylabel("Price ($)")

        # Displaying legend
        ax.legend(loc="best")

        # Redraw the canvas
        self.canvas.draw()

    def plot_forecast(self, forecast_data):
        """Helper method to plot only the forecasted data"""
        self.canvas.figure.clf()
        ax = self.canvas.figure.add_subplot(111)

        ax.plot(forecast_data, label='Forecasted Data', color='red', linestyle='-', marker='x')

        ax.set_title("Forecasted Bitcoin Price")
        ax.set_xlabel("Time")
        ax.set_ylabel("Price ($)")
        ax.legend()

        self.canvas.draw()

