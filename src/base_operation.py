# modules/base_operation.py
class BaseOperation:
    def __init__(self, name):
        self.name = name

    def execute(self):
        raise NotImplementedError("Subclasses must implement the 'execute' method.")
