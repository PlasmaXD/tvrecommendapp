# import sqlite3
# from scraper import get_program_details_from_scraper

# def connect_db():
#     return sqlite3.connect('tv_reviews.db')
# def update_program_titles():
#     conn = connect_db()
#     c = conn.cursor()
    
#     # 既存のレビューのprogram_idを取得
#     c.execute('SELECT DISTINCT program_id FROM reviews')
#     program_ids = c.fetchall()
    
#     # 各program_idについて、スクレイパーを使用してタイトルを取得し、データベースを更新
#     for (program_id,) in program_ids:
#         program_details = get_program_details_from_scraper(program_id)
#         if program_details:
#             c.execute('UPDATE reviews SET program_title = ? WHERE program_id = ?', 
#                       (program_details['title'], program_id))
    
#     conn.commit()
#     conn.close()

# if __name__ == "__main__":
#     update_program_titles()

from database import connect_db
from scraper import get_program_details_from_scraper

def update_program_supplements():
    conn = connect_db()
    c = conn.cursor()
    
    # 既存のレビューのprogram_idを取得
    c.execute('SELECT DISTINCT program_id FROM reviews')
    program_ids = c.fetchall()
    
    for (program_id,) in program_ids:
        # スクレイパーを使用して詳細を取得し、データベースを更新
        program_details = get_program_details_from_scraper(program_id)
        if program_details:
            c.execute('UPDATE reviews SET supplement = ? WHERE program_id = ?', 
                      (program_details['supplement'], program_id))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_program_supplements()
