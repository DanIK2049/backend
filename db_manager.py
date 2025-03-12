# db_manager.py
import sqlite3

DB_PATH = "devices.db"

def init_db():

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

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO known_devices (ip_address, mac_address, device_name)
        VALUES (?, ?, ?)
    """, (ip_address, mac_address, device_name))
    conn.commit()
    conn.close()

def device_exists(mac_address):

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT COUNT(*) FROM known_devices WHERE mac_address = ?
    """, (mac_address,))
    (count,) = c.fetchone()
    conn.close()
    return count > 0

def get_all_known_devices():

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT ip_address, mac_address, device_name, added_date FROM known_devices")
    rows = c.fetchall()
    conn.close()
    return rows
