# modules/operation_manager.py
class OperationManager:
    def __init__(self, logger):
        self.operations = {}
        self.logger = logger

    def register_operation(self, operation):
        """Register a new operation."""
        self.operations[operation.name] = operation

    def execute_operation(self, operation_name):
        """Execute the specified operation."""
        if operation_name in self.operations:
            self.logger.log(f"Starting operation: {operation_name}")
            self.operations[operation_name].execute()
            self.logger.log(f"Completed operation: {operation_name}")
        else:
            self.logger.log(f"Operation '{operation_name}' not found.")
