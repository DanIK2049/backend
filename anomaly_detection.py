# anomaly_detection.py
import numpy as np
from sklearn.ensemble import IsolationForest

class ExtendedAnomalyDetector:

    def __init__(self, n_estimators=50, contamination=0.1):
        self.model = IsolationForest(
            n_estimators=n_estimators,
            contamination=contamination,
            random_state=42
        )
        self.is_fitted = False

    def fit(self, X):
        """
        Обучаем модель на матрице X (n_samples x n_features).
        """
        self.model.fit(X)
        self.is_fitted = True

    def predict(self, X):
        """
        Возвращаем +1 (норма) или -1 (аномалия).
        """
        if not self.is_fitted:
            raise RuntimeError("Модель не обучена (fit)!")
        return self.model.predict(X)

    def update(self, X_new):
        """
        Возможное переобучение.
        IsolationForest не поддерживает partial_fit из коробки,
        так что можно либо хранить все данные и вызывать fit заново,
        либо сменить алгоритм (например, на нейронную сеть/кластеры).
        """
        pass
