# src/forecasting/model_manager.py
import os
from tensorflow.keras.models import load_model
from src.forecasting.lstm_model import LSTMModel

class ModelManager:
    def __init__(self, model_dir="models/"):
        self.model_dir = model_dir
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        self.models = {}

    def save_model(self, model_name, model):
        model.save(os.path.join(self.model_dir, f"{model_name}.h5"))

    def load_model(self, model_name):
        model_path = os.path.join(self.model_dir, f"{model_name}.h5")
        if os.path.exists(model_path):
            return load_model(model_path)
        else:
            raise FileNotFoundError(f"Model {model_name} not found.")

    def train_and_save_model(self, model_name, data, epochs=10):
        model = LSTMModel()  # Example: Instantiate LSTMModel
        model.train(data, epochs=epochs)
        self.save_model(model_name, model)

    def get_model(self, model_name):
        if model_name in self.models:
            return self.models[model_name]
        else:
            raise ValueError(f"Model {model_name} is not loaded or trained.")
