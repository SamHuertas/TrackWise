import os
import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv

load_dotenv()

class DBManager:
    def __init__(self):
        self.connection = pymysql.connect(
            charset="utf8mb4",
            cursorclass=DictCursor,
            db=os.getenv("DB_NAME", "defaultdb"),
            host=os.getenv("DB_HOST", "financetrackerdb-samalexishuertas1025-9ffb.b.aivencloud.com"),
            password=os.getenv("DB_PASSWORD", "AVNS_HakNwEO-ZzSCQu5U84o"),
            port=int(os.getenv("DB_PORT", "22007")),
            user=os.getenv("DB_USER", "avnadmin"),
            autocommit=True
        )

    def execute(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)

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
