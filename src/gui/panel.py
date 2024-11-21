# modules/panel.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel
from modules.operation_manager import OperationManager
from modules.operations import ETLOperation, VisualizeOperation, SimulateOperation
from modules.logger import Logger
from datetime import datetime

class Panel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control Panel")
        self.setStyleSheet("background-color: #2e2e2e; color: #ffffff;")
        self.setGeometry(900, 100, 400, 600)  # Position the panel next to the dashboard

        # Initialize Logger and Operation Manager
        self.logger = Logger()
        self.operation_manager = OperationManager(self.logger)

        # Register operations
        self.operation_manager.register_operation(ETLOperation())
        self.operation_manager.register_operation(VisualizeOperation())
        self.operation_manager.register_operation(SimulateOperation())

        # Layout Setup
        self.layout = QVBoxLayout()

        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Enter command (etl, visualize, simulate)")
        self.layout.addWidget(self.command_input)

        self.run_button = QPushButton("RUN")
        self.run_button.setStyleSheet("background-color: #5e5e5e; color: white; font-size: 14px;")
        self.run_button.clicked.connect(self.execute_command)
        self.layout.addWidget(self.run_button)

        self.status_label = QLabel("Panel: Ready")
        self.layout.addWidget(self.status_label)

        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.layout.addWidget(self.log_view)

        self.setLayout(self.layout)

    def execute_command(self):
        command = self.command_input.text().strip()
        if command:
            self.update_log(f"Executing command: {command}")
            self.operation_manager.execute_operation(command)
            self.update_log(f"Command executed: {command}")
        self.command_input.clear()

    def update_log(self, message):
        # Add a timestamp to the message
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_message = f"{timestamp} - {message}"
        self.log_view.append(full_message)
        self.logger.log(full_message)
