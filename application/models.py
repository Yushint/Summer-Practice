""" Модуль для программирования обработки моделей юзера/статей через базу данных
    SQLite. Две модели, с которой работаем --> UsersModel, ArticlesModel.
"""
from time import time
from math import floor


#def convert_data_to_binary_type(datafile):
    #with open(datafile, "rb") as binary_file:
        #binary_data = binary_file.read()
    #return binary_data

#def convert_data_to_normal_type(data, datafile):
    #with open(datafile, "wb") as normal_file:
        #normal_file.write(data)


class UsersModel:
    """Класс описания информационной модели юзера сайта."""
    def __init__(self, connection):
        """Подключение БД в конструкторе."""
        self.connection = connection
        
    def initialize_table(self):
        """Инициализация таблицы БД users."""
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(20) UNIQUE,
                             password_hash VARCHAR(128),
                             email VARCHAR(20),
                             is_admin INTEGER
                             )''')
        cursor.close()
        self.connection.commit()
        
    def insert(self, user_name, password_hash, email, is_admin=False):
        """Вставка информации о юзере в БД."""
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash, email, is_admin) 
                          VALUES (?,?,?,?)''',
                       (user_name, password_hash, email, int(is_admin)))
        cursor.close()
        self.connection.commit()
        
    def is_user_exists(self, user_name):
        """Проверка существования юзера в БД по его уникальному user_name."""
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM users WHERE user_name = ?''', [user_name])
        user_data = cursor.fetchone()
        return (True, user_data[2], user_data[0]) if user_data else (False,)
    
    def get_user(self, user_id):
        """Запрос информации о юзере через уникальный user_id."""
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM users WHERE user_id = ?''', [user_id])
        user_data = cursor.fetchone()
        return user_data
    
    def get_all_users(self):
        """Запрос всей инфы о всех юзерах в БД."""
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM users''')
        users_global_data = cursor.fetchall()
        return users_global_data
    
    def delete_user(self, user_id):
        """Удаление юзера по его уникальному user_id."""
        cursor = self.connection.cursor()
        cursor.execute('''DELETE * FROM users WHERE user_id = ?''', [user_id])
        cursor.close()
        self.connection.commit()


class ArticlesModel:
    """Класс описания информационной модели статьи. Доработать вечером
       после тестов модели юзера.
       Модель: автор, заголовок, ключевая тема, текст, рейтинг."""
    def __init__(self, connection):
        self.connection = connection
        
    def initialize_table(self):
        """Инициализация таблиц БД."""
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS articles
                            (article_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             author VARCHAR(20),
                             title VARCHAR(30),
                             key_theme NOT NULL,
                             text TEXT NOT NULL,
                             image TEXT NOT NULL,
                             time INTEGER NOT NULL)''')
        cursor.close()
        self.connection.commit()
        
    def insert(self, author, title, key_theme, text, image):
        """Вставка инфо в БД."""
        adding_time = floor(time())
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO articles
                          (author, title, key_theme, text, image, time) 
                          VALUES (?,?,?,?,?,?)''',
                       (str(author), str(title), str(key_theme), str(text), str(image),  adding_time))
        cursor.close()
        self.connection.commit()
        
    def is_article_exists(self, author, title):
        """Проверка существования статьи по автору и заголовку."""
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM articles WHERE author = ? AND title = ?''',
                       (str(author), str(title)))
        data = cursor.fetchone()
        return (True, data[0]) if data else (False,)
    
    def get_article(self, article_id):
        """Запрос статьи по id."""
        cursor = self.connection.cursor()
        cursor.execute('''SELECT article_id, author, title, key_theme, text, image FROM articles WHERE article_id = ?''', str(article_id))
        data = cursor.fetchone()
        return data
    
    def get_all_articles(self):
        """Запрос всех статей."""
        cursor = self.connection.cursor()
        cursor.execute('''SELECT article_id, author, title, key_theme, text, image FROM articles ORDER BY time DESC''')
        data = cursor.fetchmany(5)
        return data
    
    def delete_article(self, article_id):
        """Удаление статьи по id."""
        cursor = self.connection.cursor()
        cursor.execute('''DELETE * FROM articles WHERE article_id = ?''', str(article_id))
        cursor.close()
        self.connection.commit()
    
    def get_article_by_author(self, author):
        """Запрос статьи по автору."""
        cursor = self.connection.cursor()
        cursor.execute('''SELECT article_id, author, title, key_theme, text, image FROM articles WHERE author = ?''', (str(author),))
        data = cursor.fetchall()
        return data
    
    def get_article_by_key_theme(self, key_theme):
        """Запрос статьи по ключевой теме."""
        cursor = self.connection.cursor()
        cursor.execute('''SELECT article_id, author, title, key_theme, text, image FROM articles WHERE key_theme = ?''', str(key_theme))
        data = cursor.fetchall()
        return data
    
    def get_article_by_rating(self, start_rating, end_rating):
        """Запрос статьи по рейтингу."""
        cursor = self.connection.cursor()
        cursor.execute('''SELECT article_id, author, title, key_theme, text, image FROM articles WHERE rating >= ? AND rating <= ?''', (str(start_rating), str(end_rating)))
        data = cursor.fetchall()
        return data
