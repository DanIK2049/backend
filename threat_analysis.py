import time
from scapy.all import sniff
from scapy.layers.l2 import ARP
import threading

class ArpSpoofDetector:

    def __init__(self):
        self.arp_cache = {}
        self.running = False

    def arp_callback(self, packet):
        if packet.haslayer(ARP) and packet[ARP].op == 2:  # ARP reply
            sender_ip = packet[ARP].psrc
            sender_mac = packet[ARP].hwsrc

            if sender_ip in self.arp_cache:
                if self.arp_cache[sender_ip] != sender_mac:
                    print(f"[ALERT] ARP-spoof! IP={sender_ip}, MAC={sender_mac}, "
                          f"ожидалось MAC={self.arp_cache[sender_ip]}")
            else:
                self.arp_cache[sender_ip] = sender_mac

    def start(self):
        self.running = True
        sniff_thread = threading.Thread(target=self.sniff_arp, daemon=True)
        sniff_thread.start()

    def sniff_arp(self):
        sniff(filter="arp", prn=self.arp_callback, store=0)

    def stop(self):
        self.running = False
        print("ARP-spoof детектор остановлен.")


def check_in_whitelist(mac_address, whitelist):
    """
    Проверяем, есть ли MAC в белом списке (WHITELIST).
    """
    return mac_address.lower() in [m.lower() for m in whitelist]


def check_in_blacklist(mac_address, blacklist):
    """
    Проверяем, есть ли MAC в чёрном списке (BLACKLIST).
    """
    return mac_address.lower() in [m.lower() for m in blacklist]
