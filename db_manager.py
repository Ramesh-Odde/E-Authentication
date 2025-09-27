import mysql.connector
from typing import Dict




class DBManager:
    """Small wrapper around mysql.connector connection + cursor.
    NOTE: This object keeps a long-lived connection. Close it with `close()` when done."""
    def __init__(self, config: Dict):
        self._conn = mysql.connector.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            passwd=config["password"],
            database=config["database"],
        )
        self._cursor = (self._conn.cursor(buffered=True))
    @property
    def cursor(self):
        return self._cursor
    @property
    def connection(self):
        return self._conn
    def commit(self):
        self._conn.commit()


    def close(self):
        try:
            self._cursor.close()
        except Exception:
            pass
        try:
            self._conn.close()
        except Exception:
             pass