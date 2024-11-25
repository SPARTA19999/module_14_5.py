import sqlite3


# Функция для инициализации базы данных и создания таблицы Users
def initiate_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Создание таблицы Users, если она ещё не существует
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL DEFAULT 1000
    )
    """)
    conn.commit()
    conn.close()


# Функция для добавления нового пользователя
def add_user(username, email, age):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Вставка нового пользователя в таблицу
    cursor.execute("""
    INSERT INTO Users (username, email, age, balance) 
    VALUES (?, ?, ?, ?)
    """, (username, email, age, 1000))  # Баланс по умолчанию 1000
    conn.commit()
    conn.close()


# Функция для проверки, существует ли пользователь с таким именем
def is_included(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Проверка на наличие пользователя в базе
    cursor.execute("SELECT COUNT(*) FROM Users WHERE username = ?", (username,))
    count = cursor.fetchone()[0]

    conn.close()

    return count > 0
