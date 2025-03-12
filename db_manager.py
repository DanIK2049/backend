# db_manager.py
import sqlite3

DB_PATH = "devices.db"

def init_db():
    """
    Инициализация БД и создание таблицы known_devices, если её ещё нет.
    Структура таблицы:
      id (PRIMARY KEY) - уникальный идентификатор
      ip_address       - IP-адрес устройства
      mac_address      - MAC-адрес
      device_name      - (опционально) имя устройства
      added_date       - дата/время добавления
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS known_devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            mac_address TEXT,
            device_name TEXT,
            added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_known_device(ip_address, mac_address, device_name=""):
    """
    Добавляем новое устройство в таблицу known_devices.
    Если нужно, можно сначала проверить, не существует ли там этот MAC.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO known_devices (ip_address, mac_address, device_name)
        VALUES (?, ?, ?)
    """, (ip_address, mac_address, device_name))
    conn.commit()
    conn.close()

def device_exists(mac_address):
    """
    Проверяем, есть ли устройство в БД (по MAC).
    Возвращает True, если запись существует.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT COUNT(*) FROM known_devices WHERE mac_address = ?
    """, (mac_address,))
    (count,) = c.fetchone()
    conn.close()
    return count > 0

def get_all_known_devices():
    """
    Возвращаем список всех «известных» устройств.
    Возвращает список кортежей (ip_address, mac_address, device_name, added_date).
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT ip_address, mac_address, device_name, added_date FROM known_devices")
    rows = c.fetchall()
    conn.close()
    return rows
