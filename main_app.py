import sys
import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget
from PyQt5.QtCore import QTimer, Qt
import threading
import mplcursors  # For hover functionality
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from src.operations.etl import ETLOperation  # Import ETL classes

# Set dark style for matplotlib
import matplotlib.style as style
style.use('dark_background')

class LineChart(FigureCanvas):
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.figure = Figure(figsize=(10, 6))
        super().__init__(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Bitcoin Price Over Time", color='white')
        self.ax.set_xlabel("Time", color='white')
        self.ax.set_ylabel("Price (USD)", color='white')

        self.x_data = []
        self.y_data = []
        self.dots = None  # Placeholder for dot markers

    def update_chart(self):
        """
        Update the chart with the latest data from the CSV file.
        """
        if not os.path.exists(self.csv_path):
            return

        # Load data
        data = pd.read_csv(self.csv_path)

        if len(data) == 0:
            return

        # Plot data
        self.ax.clear()

        # Add new x, y data points for chart
        self.x_data = data["Date"]
        self.y_data = data["Close"]

        # Plot the full dataset
        self.ax.plot(self.x_data, self.y_data, label="Price", color="gray", linestyle="-", linewidth=1)

        # Highlight the latest point with dots
        if len(data) > 1:
            latest_price = data.iloc[-1]["Close"]
            previous_price = data.iloc[-2]["Close"]
            color = "red" if latest_price > previous_price else "blue"
            self.dots = self.ax.plot(self.x_data.iloc[-1], latest_price, marker="o", color=color, markersize=10)

        # Set the axis to fit the full range of data (no panning/zooming)
        self.ax.set_xlim(0, len(data))  # Show the entire range of x data
        self.ax.set_ylim(min(self.y_data) - 1000, max(self.y_data) + 1000)  # Adjust Y axis to avoid crowding

        # Remove x-axis for a cleaner look (no axis)
        self.ax.set_xticklabels([])  # Hide x-axis ticks and labels

        # Show the hover tool
        cursor = mplcursors.cursor(self.ax, hover=True)

        # Update tick parameters for dark theme
        self.ax.tick_params(axis='both', colors='white')

        # Set grid and background for dark theme
        self.ax.grid(True, color='gray', linestyle='--', linewidth=0.5)
        self.ax.set_facecolor('#2E2E2E')  # Dark background for the plot area

        self.ax.legend()
        self.figure.tight_layout()
        self.draw()

        # Remove the message box code to avoid conflicts
        cursor.connect("add", self.on_hover)

    def on_hover(self, sel):
        """
        Display the hovered data point on the status bar.
        """
        # Get the x and y coordinates of the point
        x, y = sel.target
        time_str = str(self.x_data[int(x)])  # Convert to date string
        price_str = f"{y:.2f}"

        # Print hover details to the console or status bar (no message box)
        print(f"Hovered over: Date: {time_str}, Price: ${price_str}")


class Dashboard(QWidget):
    def __init__(self, csv_path):
        super().__init__()
        self.csv_path = csv_path

        # Layout for the dashboard
        self.layout = QVBoxLayout(self)
        self.label = QLabel("Bitcoin Price Dashboard")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: white;")  # Label text color for dark theme

        # Add line chart
        self.chart = LineChart(csv_path)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.chart)

        # Timer for real-time updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_dashboard)
        self.timer.start(1000)  # Update every 1 second

        self.update_dashboard()  # Initial load

    def update_dashboard(self):
        """
        Update the dashboard's chart.
        """
        self.chart.update_chart()


class MainApp(QMainWindow):
    def __init__(self, csv_path):
        super().__init__()
        self.setWindowTitle("Bitcoin Forecasting and Trading Dashboard")
        self.setGeometry(100, 100, 800, 600)

        # Set the dark theme for the window background
        self.setStyleSheet("background-color: #2E2E2E; color: white;")

        # Set Dashboard as the central widget
        self.dashboard = Dashboard(csv_path)
        self.setCentralWidget(self.dashboard)


def start_etl(csv_path):
    """
    Start the ETL process in a separate thread.
    """
    etl = ETLOperation(csv_path=csv_path)
    etl.save_initial_data()  # Save initial data
    etl.track_price()        # Start tracking price changes


if __name__ == "__main__":
    csv_file_path = os.path.join("data", "bitcoin_data_2024.csv")
    os.makedirs("data", exist_ok=True)  # Ensure the directory exists

    # Start ETL in a separate thread
    etl_thread = threading.Thread(target=start_etl, args=(csv_file_path,))
    etl_thread.daemon = True  # Daemonize the thread to close it with the main app
    etl_thread.start()

    # Start the Dashboard
    app = QApplication(sys.argv)
    main_window = MainApp(csv_path=csv_file_path)
    main_window.show()
    sys.exit(app.exec_())
