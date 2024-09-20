import sqlite3

def create_table():
    conn = sqlite3.connect('payment.db')

    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS id (
            id INTEGER PRIMARY KEY AUTOINCREMENT
            
        )
    """)
    conn.commit()
    conn.close()
create_table()

def insert(id):
    conn = sqlite3.connect('payment.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO id (id) VALUES (?)", (id,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass

    conn.close()



def get_id_by_id(id):
    conn = sqlite3.connect('payment.db')
    c = conn.cursor()

    c.execute("SELECT * FROM id WHERE id = ?", (id,))
    rows = c.fetchall()
    conn.close()
    return rows
