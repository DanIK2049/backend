import time
import threading
import numpy as np
from network_info import scan_network, get_own_network_info
from threat_analysis import ArpSpoofDetector
from anomaly_detection import ExtendedAnomalyDetector

def send_alert(msg):
    print("[ALERT]", msg)

def start_arp_spoof_detector():
    detector = ArpSpoofDetector()
    detector.start()

def monitor_anomalies():
    model = ExtendedAnomalyDetector(n_estimators=50, contamination=0.1)
    normal_data = np.random.normal(1000, 300, (10, 3))
    model.fit(normal_data)
    while True:

        test_data = np.array([
            [900, 1100, 950],
            [100000, 99999, 20000]
        ])
        preds = model.predict(test_data)
        for i, pred in enumerate(preds):
            if pred == -1:
                if i == 0:
                    send_alert("Anomaly detected: Unknown")
                else:
                    send_alert("Anomaly detected: DDoS Attack")
        time.sleep(10)

def monitor_network():
    while True:
        devices = scan_network("192.168.1.0/24")
        print("\nScan result (ARP):", len(devices), "devices")
        for d in devices:
            print("IP =", d["ip"], "MAC =", d["mac"])
        time.sleep(10)

def main():
    ip, mac = get_own_network_info()
    print("Current host IP =", ip, "MAC =", mac)
    start_arp_spoof_detector()
    t_anom = threading.Thread(target=monitor_anomalies, daemon=True)
    t_anom.start()
    monitor_network()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
        exit(0)
