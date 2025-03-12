import requests
class RouterAPI:

    def __init__(self, base_url, username, password):

        self.base_url = base_url
        self.session = requests.Session()


    def block_mac(self, mac_address):

        print(f"[INFO] Пытаемся заблокировать MAC {mac_address} на роутере...")

        pass
