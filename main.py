import time
import threading

from network_info import scan_network, get_own_network_info
from threat_analysis import ArpSpoofDetector
from self_learning_ml import start_self_learning_ml

def main():
    # Шаг 1: Показываем IP/MAC текущего хоста
    my_ip, my_mac = get_own_network_info()
    print(f"[INFO] Current host IP={my_ip}, MAC={my_mac}")

    # Шаг 2: Однократное сканирование сети, выводим список устройств
    devices = scan_network("192.168.1.0/24")
    print(f"[INFO] Found {len(devices)} devices in Wi-Fi:")
    for idx, dev in enumerate(devices, start=1):
        print(f"   {idx}. IP={dev['ip']}, MAC={dev['mac']}")

    # Шаг 3: Запускаем поток ARP-spoof детектора
    # Он будет выводить сообщения в реальном времени ТОЛЬКО при обнаружении атаки
    def run_arp_spoof():
        detector = ArpSpoofDetector()
        detector.start()
        while True:
            time.sleep(1)
    t_arp = threading.Thread(target=run_arp_spoof, daemon=True)
    t_arp.start()

    # Шаг 4: Запускаем самообучающийся ML (IsolationForest) в отдельном потоке
    # Он будет переобучаться каждые 30 сек и выводить,
    # на скольких данных обучился и нашёл ли аномалии (DDoS и т.д.)
    t_ml = threading.Thread(target=start_self_learning_ml, daemon=True)
    t_ml.start()

    # Основной поток "оживает" до Ctrl+C
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user (Ctrl+C).")

if __name__ == "__main__":
    main()
