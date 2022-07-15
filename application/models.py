""" Модуль для программирования обработки моделей юзера/статей через базу данных
    SQLite. Две модели, с которой работаем --> UsersModel, ArticlesModel.
"""
from time import time
from math import floor


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
                             is_admin INTEGER,
                             avatar TEXT NOT NULL
                             )''')
        cursor.close()
        self.connection.commit()
        
    def insert(self, user_name, password_hash, email, is_admin=False, avatar="../static/img\default.png"):
        """Вставка информации о юзере в БД."""
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash, email, is_admin, avatar) 
                          VALUES (?,?,?,?,?)''',
                       (user_name, password_hash, email, int(is_admin), avatar))
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
    
    def get_user_id(self, user_name):
        """Получение id пользователя по уникальному имени."""
        cursor = self.connection.cursor()
        cursor.execute('''SELECT user_id FROM users WHERE user_name = ?''', [user_name])
        user_id = cursor.fetchone()
        return str(user_id[0])
    
    def get_all_users(self):
        """Запрос всей инфы о всех юзерах в БД."""
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM users''')
        users_global_data = cursor.fetchall()
        return users_global_data
    
    def delete_user(self, user_id):
        """Удаление юзера по его уникальному user_id."""
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM users WHERE user_id = ?''', [user_id])
        cursor.close()
        self.connection.commit()
        
    def set_avatar(self, user_id, avatar):
        """ Обновление аватара пользователя. """
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE users SET avatar = ? WHERE user_id = ?''', (avatar, user_id))
        cursor.close()
        self.connection.commit()


class ArticlesModel:
    """Класс описания информационной модели статьи. Доработать вечером
       после тестов модели юзера.
       Модель: автор, заголовок, ключевая тема, текст, превью, 
       верхнее и нижнее изображения, время добавления.
    """
    def __init__(self, connection):
        self.connection = connection
        
    def initialize_table(self):
        """Инициализация таблиц БД articles."""
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS articles
                            (article_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             author VARCHAR(20),
                             title TEXT NOT NULL,
                             key_theme TEXT NOT NULL,
                             text TEXT NOT NULL,
                             preview_image TEXT NOT NULL,
                             header_image TEXT NOT NULL,
                             bottom_image TEXT NOT NULL,
                             time INTEGER NOT NULL)''')
        cursor.close()
        self.connection.commit()
        
    def insert(self, author, title, key_theme, text, preview_image, header_image, bottom_image):
        """Вставка инфо в БД."""
        adding_time = floor(time())
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO articles
                          (author, title, key_theme, text, preview_image, header_image, bottom_image, time) 
                          VALUES (?,?,?,?,?,?,?,?)''',
                       (str(author), str(title), str(key_theme), str(text), preview_image, header_image, bottom_image, adding_time))
        cursor.close()
        self.connection.commit()
        
    def is_article_exists(self, article_id):
        """Проверка существования статьи по автору и заголовку."""
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM articles WHERE article_id = ?''', [article_id])
        data = cursor.fetchone()
        return (True, data[0]) if data else (False,)
    
    def get_article(self, article_id):
        """Запрос статьи по id."""
        cursor = self.connection.cursor()
        cursor.execute('''SELECT article_id, author, title, key_theme, text, preview_image, header_image, bottom_image FROM articles WHERE article_id = ?''', str(article_id))
        data = cursor.fetchone()
        return data
    
    def get_all_articles(self, amount):
        """Запрос всех статей."""
        cursor = self.connection.cursor()
        cursor.execute('''SELECT article_id, author, title, key_theme, text, preview_image, header_image, bottom_image FROM articles ORDER BY time DESC''')
        if amount == 0:
            data = cursor.fetchall()
        else:
            data = cursor.fetchmany(amount)
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
        cursor.execute('''SELECT article_id, author, title, key_theme, text, preview_image, header_image, bottom_image FROM articles WHERE author = ?''', (str(author),))
        data = cursor.fetchall()
        return data
    
    def get_article_by_key_theme(self, key_theme):
        """Запрос статьи по ключевой теме."""
        cursor = self.connection.cursor()
        cursor.execute('''SELECT article_id, author, title, key_theme, text, preview_image, header_image, bottom_image FROM articles WHERE key_theme = ?''', str(key_theme))
        data = cursor.fetchall()
        return data
    

class SelectedArticlesModel:
    """ Модель избранных статей пользователя. """
    def __init__(self, connection):
        self.connection = connection
        
    def initialize_table(self):
        """Инициализация таблицы БД selected_articles."""
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS selected_articles 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             host_user_id INTEGER, 
                             selected_article_id INTEGER)''')
        cursor.close()
        self.connection.commit()
        
    def insert(self, host_user_id, selected_article_id):
        """ Добавление статьи в избранное. """
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO selected_articles (host_user_id, selected_article_id) VALUES (?, ?)''', (int(host_user_id), int(selected_article_id)))
        cursor.close()
        self.connection.commit()
        
    def is_selected_article_exists(self, host_user_id, selected_article_id):
        """ Проверка наличия статьи в избранном. """
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM selected_articles WHERE host_user_id = ? AND selected_article_id = ?''', (host_user_id, selected_article_id))
        data = cursor.fetchone()
        return (True, data[1]) if data else (False,)
        
    def get_selected_articles_id(self, host_user_id):
        """ Получение id всех избранных статей. """
        cursor = self.connection.cursor()
        cursor.execute('''SELECT selected_article_id FROM selected_articles WHERE host_user_id = ?''', [host_user_id])
        selected_articles_id_data = cursor.fetchall()
        data = [tuple_id[0] for tuple_id in selected_articles_id_data]
        return data
    
    def delete_selected_article(self, selected_article_id):
        """ Удаление статьи из избранного по её id. """
        cursor = self.connection.cursor()
        cursor.execute('''DELETE * FROM selected_articles WHERE selected_article_id = ?''', [selected_article_id])
        cursor.close()
        self.connection.commit()
        
