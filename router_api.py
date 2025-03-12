# router_api.py
import requests

class RouterAPI:
    """
    Пример взаимодействия с роутером через HTTP/REST API.
    У каждого роутера свой формат запросов: изучайте документацию производителя.
    """
    def __init__(self, base_url, username, password):
        """
        :param base_url: адрес роутера, например "http://192.168.1.1"
        :param username: логин
        :param password: пароль
        """
        self.base_url = base_url
        self.session = requests.Session()
        # Примерная авторизация:
        # self.session.post(f"{self.base_url}/login", data={"username": username, "password": password})

    def block_mac(self, mac_address):
        """
        Пример запроса для блокировки MAC.
        Реальные роутеры могут требовать PUT или POST с конкретными полями.
        """
        print(f"[INFO] Пытаемся заблокировать MAC {mac_address} на роутере...")
        # Например:
        # response = self.session.post(f"{self.base_url}/api/block_mac", json={"mac": mac_address})
        #
        # if response.status_code == 200:
        #     print("[OK] MAC успешно заблокирован.")
        # else:
        #     print(f"[ERROR] Роутер вернул {response.status_code}, не удалось заблокировать MAC.")
        pass
