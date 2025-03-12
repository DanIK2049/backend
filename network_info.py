import psutil
import socket
from scapy.layers.l2 import ARP, Ether,srp
import nmap  # Убедитесь, что установили пакет python-nmap


def get_own_network_info():
    """
    Возвращает (ip_address, mac_address) текущего хоста.

    На Windows MAC может иметь addr.family == 17 (psutil.AF_LINK).
    На Linux/macOS - psutil.AF_LINK или AF_PACKET.
    """
    ip_address = None
    mac_address = None

    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ip_address = addr.address
            if addr.family == psutil.AF_LINK or addr.family == 17:
                mac_address = addr.address

        if ip_address and mac_address:
            break

    return ip_address, mac_address


def scan_network(ip_range="192.168.1.0/24"):
    """
    Сканируем сеть по ARP, возвращаем [{'ip': .., 'mac': ..}, ...].
    """
    devices = []
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = srp(packet, timeout=3, verbose=0)[0]

    for sent, received in result:
        devices.append({
            'ip': received.psrc,
            'mac': received.hwsrc
        })
    return devices


def scan_ports_extended(ip_address):
    """
    Запускаем nmap со следующими опциями:
      -sS (SYN scan)
      -T4 (скорость)
      -Pn (не пингуем)
      -sV (определение версий сервисов)
      -O (определение ОС)
    Возвращаем структуру вида:
    {
      "ports": [
         {"port": 22, "protocol": "tcp", "service": "ssh", "version": "OpenSSH 8.2"},
         ...
      ],
      "os_match": [
         {"name": "Linux 3.2 - 4.9", "accuracy": "90", ...},
         ...
      ]
    }
    """
    nm = nmap.PortScanner()
    nm.scan(ip_address, arguments="-sS -T4 -Pn -sV -O")
    results = {
        "ports": [],
        "os_match": []
    }

    if ip_address in nm.all_hosts():
        host_data = nm[ip_address]

        for proto in host_data.all_protocols():
            for port in host_data[proto]:
                port_data = host_data[proto][port]
                if port_data["state"] == "open":
                    results["ports"].append({
                        "port": port,
                        "protocol": proto,
                        "service": port_data.get("name"),
                        "version": port_data.get("version")
                    })

        if "osmatch" in host_data:
            results["os_match"] = host_data["osmatch"]

    return results