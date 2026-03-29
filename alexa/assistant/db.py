import sqlite3

DB_FILE = "assistant_memory.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY, note TEXT)")
    conn.commit()
    conn.close()

def save_memory(note: str):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO memory(note) VALUES (?)", (note,))
    conn.commit()
    conn.close()

def get_memory():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT note FROM memory")
    rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]
