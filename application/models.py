""" Модуль для программирования обработки моделей юзера/статей через базу данных
    SQLite. Две модели, с которой работаем --> UsersModel, ArticlesModel.
"""

class UsersModel:
    """Класс описания информационной модели юзера сайта."""
    def __init__(self, connection):
        """Подключение БД в конструкторе."""
        self.connection = connection
        
    def initialize_table(self):
        """Инициализация таблицы БД users."""
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
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
        return (True, user_data[2], user_data[0]) if user_data else (False)
    
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
        """Удаление бюзера по его уникальному user_id."""
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM users WHERE user_id = ?''', [user_id])
        cursor.close()
        self.connection.commit()


class ArticlesModel:
    """Класс описания информационной модели статьи. Доработать вечером
       после тестов модели юзера."""
    def __init__(self, connection):
        pass
        
    def initialize_table(self):
        pass
        
    def insert(self):
        pass
        
    def is_article_exists(self):
        pass
    
    def get_article(self):
        pass
    
    def get_all_articles(self):
        pass
    
    def delete_article(self, article_id):
        pass
    
    def get_article_by_author(self):
        pass
    
    def get_article_by_theme(self):
        pass
    
        
