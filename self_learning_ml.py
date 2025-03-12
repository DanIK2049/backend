# self_learning_ml.py
import time
import random
import numpy as np
from sklearn.ensemble import IsolationForest

from db_manager import init_db, insert_metrics, get_all_metrics

class SelfLearningAnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(n_estimators=50, contamination=0.1, random_state=42)
        self.is_fitted = False

    def fit(self, X):
        self.model.fit(X)
        self.is_fitted = True

    def predict(self, X):
        if not self.is_fitted:
            raise RuntimeError("Model not fitted yet.")
        return self.model.predict(X)

def generate_fake_metrics():
    # (В реальном проекте заменить на реальную статистику Wi-Fi устройств)
    dev_ids = ["device1", "device2", "device3"]
    dev_id = random.choice(dev_ids)
    rx = random.gauss(1000, 300)
    tx = random.gauss(1000, 300)
    conns = random.gauss(10, 5)
    return dev_id, rx, tx, conns

def start_self_learning_ml():
    print("[ML] Self-learning ML thread started. (Every 30s)")

    init_db()
    detector = SelfLearningAnomalyDetector()

    try:
        while True:

            for _ in range(3):
                dev_id, rx, tx, conns = generate_fake_metrics()
                insert_metrics(dev_id, rx, tx, conns)

            # Загружаем все метрики
            rows = get_all_metrics()
            if rows:
                data = np.array(rows, dtype=float)
                detector.fit(data)
                print(f"[ML] Model re-trained on {len(data)} data points.")

                # Проверяем "DDoS" - точку с очень большим трафиком
                test_ddos = np.array([[99999, 99999, 50]])
                pred = detector.predict(test_ddos)[0]
                if pred == -1:
                    print("[ALERT] Possible DDoS Attack!")
            else:
                print("[ML] No data to train on yet.")

            # Ждём 30 сек, прежде чем снова переобучать
            time.sleep(30)
    except KeyboardInterrupt:
        print("\n[ML] Stopped by user (Ctrl+C).")
