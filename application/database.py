import sqlite3
"""
   Модуль для работы с базой данных SQLite. Используется для подключения к 
   API Flask.
"""

class DB:
    def __init__(self):
        """В конструкторе создаём базу данных 'database00.db'"""
        connection = sqlite3.connect("database00.db", check_same_thread=False)
        self.conn = connection
        
    def get_connection(self):
        """Возвращаем текущий сonnection через self.conn, который нужен будет для
           подклчючения информационных моделей user/article.
        """
        return self.conn
    
    def __del__(self):
        """При прекращении работы сервера вызываем деструктор. Все соединения 
           закрываются.
        """
        self.conn.close()
