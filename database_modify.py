# import sqlite3

# def connect_db():
#     return sqlite3.connect('tv_reviews.db')

# def add_column():
#     conn = connect_db()
#     c = conn.cursor()
    
#     # reviewsテーブルにprogram_titleカラムを追加
#     c.execute('ALTER TABLE reviews ADD COLUMN program_title TEXT')
    
#     # programsテーブルが存在しない場合は作成
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS programs (
#             program_id TEXT PRIMARY KEY,
#             url TEXT,
#             title TEXT,
#             supplement TEXT
#         )
#     ''')
    
#     conn.commit()
#     conn.close()

# if __name__ == "__main__":
#     add_column()
import sqlite3

def connect_db():
    return sqlite3.connect('tv_reviews.db')

def add_columns():
    conn = connect_db()
    c = conn.cursor()
    
    # reviewsテーブルにsupplementカラムを追加
    c.execute('ALTER TABLE reviews ADD COLUMN supplement TEXT')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_columns()
