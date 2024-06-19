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
    c.execute('''
        CREATE TABLE IF NOT EXISTS programs (
            program_id TEXT PRIMARY KEY,
            url TEXT,
            title TEXT,
            supplement TEXT
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
        c.execute('INSERT OR IGNORE INTO favorites (user_id, program_id) VALUES (?, ?, ?)', (user_id, program_id))
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

def get_all_reviews():
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute('SELECT user_id, program_id, rating FROM reviews')
        reviews = c.fetchall()
        conn.close()
        return reviews
    except Exception as e:
        print(f"Error fetching all reviews: {e}")
        return []

def get_program_details(program_id):
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute('SELECT url, title, supplement FROM programs WHERE program_id = ?', (program_id,))
        program_details = c.fetchone()
        conn.close()
        if program_details:
            return {'url': program_details[0], 'title': program_details[1], 'supplement': program_details[2]}
        else:
            return {'url': program_id, 'title': f'Program {program_id}', 'supplement': f'Details of Program {program_id}'}
    except Exception as e:
        print(f"Error fetching program details: {e}")
        return {'url': program_id, 'title': f'Program {program_id}', 'supplement': f'Details of Program {program_id}'}

def add_program(program_id, url, title, supplement):
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO programs (program_id, url, title, supplement) VALUES (?, ?, ?, ?)',
                  (program_id, url, title, supplement))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error adding program: {e}")
