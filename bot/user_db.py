import sqlite3
from bot.loader import user_db


def create_users_db():
    """Создает базу данных для хранения информации о пользователях"""
    conn = sqlite3.connect(user_db)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            balance INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def create_user(user_id, balance=0):
    """Создает нового пользователя в базе данных"""
    conn = sqlite3.connect(user_db)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (id, balance) VALUES (?, ?)", (user_id, balance))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Пользователь с ID {user_id} уже существует.")
    conn.close()

def get_user(user_id):
    """Получает информацию о пользователе по его id"""
    conn = sqlite3.connect(user_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def add_user_rub(user_id, new_balance):
    """Обновляет количество токенов пользователя"""
    conn = sqlite3.connect(user_db)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (new_balance, user_id))
    conn.commit()
    conn.close()

create_users_db()