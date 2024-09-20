import json
import sqlite3
from loader import stack_db


# Функция для создания таблицы
def create_table():
    conn = sqlite3.connect(stack_db)

    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS stack (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            audio_path TEXT,
            photo_id TEXT,
            text TEXT,
            user_id INTEGER,
            gpt TEXT,
            status INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
create_table()

# Функция для вставки данных в таблицу
def insert_data(time, audio_path, text, user_id, gpt, status=0):
    conn = sqlite3.connect(stack_db)
    c = conn.cursor()
    c.execute("INSERT INTO stack (time, audio_path, text, user_id, gpt, status) VALUES (?, ?, ?, ?, ?, ?)",
              (time, audio_path, text, user_id, gpt, status))
    last_row_id = c.lastrowid
    conn.commit()
    conn.close()
    return last_row_id


def delete_by_id(row_id):
    conn = sqlite3.connect(stack_db)
    c = conn.cursor()

    c.execute("DELETE FROM stack WHERE id = ?", (row_id,))
    conn.commit()
    conn.close()

# Функция для выборки данных из таблицы
def select_data(status=1):
    conn = sqlite3.connect(stack_db)
    c = conn.cursor()

    c.execute("SELECT * FROM stack WHERE status = ?", (status, ))
    data = c.fetchall()
    conn.close()
    return data

def get_data(user_id, status=3):
    conn = sqlite3.connect(stack_db)
    c = conn.cursor()

    c.execute("SELECT * FROM stack WHERE status = ? AND user_id = ?", (status, user_id))
    data = c.fetchall()
    conn.close()
    return data

# Функция для обновления статуса сообщения
def update_status(message_id, new_status):
    conn = sqlite3.connect(stack_db)
    c = conn.cursor()
    c.execute("UPDATE stack SET status = ? WHERE id = ?", (new_status, message_id))
    conn.commit()
    conn.close()


def add_comment(text, id):
    """
    Эта функция добавляет комментарий в таблицу "stack" по заданному ID.

    Аргументы:
    comment (str) - комментарий, который нужно добавить
    id (int) - ID записи, в которую нужно добавить комментарий
    """
    conn = sqlite3.connect(stack_db)
    c = conn.cursor()

    # Обновляем запись в таблице "stack" с заданным ID, добавляя туда комментарий
    c.execute("UPDATE stack SET text = ? WHERE id = ?", (text, id))

    # Сохраняем изменения
    conn.commit()
    conn.close()

#
# def add_photo_id(photo_id, id):
#     l = json.dumps(photo_id)
#     conn = sqlite3.connect('stack.db')
#     c = conn.cursor()
#
#     # Обновляем запись в таблице "stack" с заданным ID, добавляя туда ID фотографии
#     c.execute("UPDATE stack SET photo_id = ? WHERE id = ?", (l, id))
#
#     # Сохраняем изменения
#     conn.commit()
#     conn.close()


def add_photo_ids(photo_ids, user_id):
    conn = sqlite3.connect(stack_db)
    c = conn.cursor()

    # Получаем существующий список photo_id для данного user_id
    c.execute("SELECT photo_id FROM stack WHERE user_id = ?", (user_id,))
    existing_photo_ids = c.fetchone()
    if existing_photo_ids:
        # Загружаем существующий список photo_id из JSON-строки
        photo_id_list = json.loads(existing_photo_ids[0])
        # Добавляем новые photo_id к существующему списку
        photo_id_list.extend(photo_ids)
        new_photo_id = json.dumps(photo_id_list)
    else:
        # Создаем новый список с photo_id
        new_photo_id = json.dumps(photo_ids)

    # Обновляем или вставляем запись в базе данных
    c.execute("SELECT * FROM stack WHERE user_id = ?", (user_id,))
    if c.fetchone():
        # Обновляем существующую запись
        c.execute("UPDATE stack SET photo_id = ? WHERE user_id = ?", (new_photo_id, user_id))
    else:
        # Вставляем новую запись
        c.execute("INSERT INTO stack (photo_id, user_id) VALUES (?, ?)", (new_photo_id, user_id))
    conn.commit()
    conn.close()

def select_data_for_user(user_id, status=3):
    conn = sqlite3.connect(stack_db)
    c = conn.cursor()

    c.execute("SELECT * FROM stack WHERE status = ? AND user_id = ?", (status, user_id))
    data = c.fetchall()
    conn.close()
    return data