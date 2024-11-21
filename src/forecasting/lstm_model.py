# src/forecasting/lstm_model.py
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler

class LSTMModel:
    def __init__(self):
        self.model = None
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    def prepare_data(self, data, time_steps=60):
        data = self.scaler.fit_transform(data)
        X, y = [], []
        for i in range(time_steps, len(data)):
            X.append(data[i-time_steps:i, 0])
            y.append(data[i, 0])
        return np.array(X), np.array(y)

    def build_model(self, input_shape):
        self.model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(input_shape[1], 1)),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        self.model.compile(optimizer='adam', loss='mean_squared_error')

    def train(self, data, epochs=10, batch_size=32):
        X, y = self.prepare_data(data)
        X = X.reshape((X.shape[0], X.shape[1], 1))
        self.build_model(X.shape)
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size)

    def forecast(self, data):
        X, _ = self.prepare_data(data)
        X = X.reshape((X.shape[0], X.shape[1], 1))
        return self.model.predict(X)
