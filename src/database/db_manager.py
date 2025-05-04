import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

class DBManager:
    def __init__(self):
        self.timeout = 10
        self.connection = pymysql.connect(
            charset="utf8mb4",
            connect_timeout=self.timeout,
            cursorclass=pymysql.cursors.DictCursor,
            db=os.getenv("DB_NAME"),
            host=os.getenv("DB_HOST"),
            password=os.getenv("DB_PASSWORD"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            read_timeout=self.timeout,
            write_timeout=self.timeout,
        )

    def execute(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
        self.connection.commit()

    def fetchall(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def fetchone(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    def close(self):
        self.connection.close()
