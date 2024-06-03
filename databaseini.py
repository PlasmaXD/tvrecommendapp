import sqlite3

def connect_db():
    return sqlite3.connect('tv_reviews.db')

def create_tables():
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            user_name TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            program_id TEXT,
            user_id TEXT,
            rating INTEGER,
            review_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            user_id TEXT,
            program_id TEXT,
            PRIMARY KEY (user_id, program_id)
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()

