# main_app.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout
from modules.dashboard import Dashboard
from modules.panel import Panel  # Assuming the Panel module exists

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bitcoin Forecasting and Trading Application")
        self.setGeometry(100, 100, 1600, 800)  # Adjust window size

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout for Dashboard and Panel
        layout = QHBoxLayout()
        self.dashboard = Dashboard()
        self.panel = Panel()
        layout.addWidget(self.dashboard)
        layout.addWidget(self.panel)

        # Set the layout
        central_widget.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
