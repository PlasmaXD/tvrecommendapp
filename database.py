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

def add_user(user_id, user_name):
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO users (user_id, user_name) VALUES (?, ?)', (user_id, user_name))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error adding user: {e}")

def add_review(program_id, user_id, rating, review_text):
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute('INSERT INTO reviews (program_id, user_id, rating, review_text) VALUES (?, ?, ?, ?)', (program_id, user_id, rating, review_text))
        conn.commit()
        conn.close()
        print(f"Review added: {program_id}, {user_id}, {rating}, {review_text}")
    except Exception as e:
        print(f"Error adding review: {e}")

def get_reviews(program_id):
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute('SELECT user_id, rating, review_text, created_at FROM reviews WHERE program_id = ?', (program_id,))
        reviews = c.fetchall()
        conn.close()
        return reviews
    except Exception as e:
        print(f"Error fetching reviews: {e}")
        return []

def add_favorite(user_id, program_id):
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO favorites (user_id, program_id) VALUES (?, ?)', (user_id, program_id))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error adding favorite: {e}")

def get_user_favorites(user_id):
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute('SELECT program_id FROM favorites WHERE user_id = ?', (user_id,))
        favorites = c.fetchall()
        conn.close()
        return [fav[0] for fav in favorites]
    except Exception as e:
        print(f"Error fetching user favorites: {e}")
        return []
