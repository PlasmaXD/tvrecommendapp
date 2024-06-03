

### ディレクトリ構成
ディレクトリを以下のように設定します：

```
tvapp/
├── app.py
├── database.py
├── scraper.py
└── utils.py
```

### 各ファイルの内容

#### `app.py`
```python
import streamlit as st
from scraper import get_program_details
from database import add_review, get_reviews
from utils import extract_program_id

def review_form(program_id):
    form_key = f"review_form_{program_id}"
    with st.form(key=form_key):
        user_id = st.number_input("ユーザーID", min_value=1, step=1)
        rating = st.slider("評価", 1, 5, 3)
        review_text = st.text_area("レビューを入力してください")
        submit_button = st.form_submit_button("レビューを投稿")
        
        if submit_button:
            add_review(program_id, user_id, rating, review_text)
            st.success("レビューが投稿されました！")

def show_reviews(program_id):
    reviews = get_reviews(program_id)
    if reviews:
        st.subheader("レビュー")
        for review in reviews:
            st.write(f"ユーザーID: {review[0]}, 評価: {review[1]}星, レビュー: {review[2]}, 投稿日: {review[3]}")
    else:
        st.write("この番組にはまだレビューがありません。")

def main():
    st.title('番組情報と共演者検索')
    search_word = st.text_input("検索ワードを入力してください", "")
    if st.button('検索'):
        program_data = get_program_details(search_word)
        for program in program_data:
            program_id = extract_program_id(program['url'])  # URLから番組IDを抽出
            st.write(f"番組名: {program['title']}")
            st.write(f"情報: {program['supplement']}")
            st.write("共演者:")
            for name in program['cast_names']:
                st.write(f" - {name}")
            st.write("\n")

            # レビュー投稿フォームとレビュー表示
            review_form(program_id)
            show_reviews(program_id)

if __name__ == "__main__":
    main()
```

#### `database.py`
```python
import sqlite3

def connect_db():
    return sqlite3.connect('tv_reviews.db')

def add_review(program_id, user_id, rating, review_text):
    conn = connect_db()
    c = conn.cursor()
    c.execute('INSERT INTO reviews (program_id, user_id, rating, review_text) VALUES (?, ?, ?, ?)', (program_id, user_id, rating, review_text))
    conn.commit()
    conn.close()

def get_reviews(program_id):
    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT user_id, rating, review_text, created_at FROM reviews WHERE program_id = ?', (program_id,))
    reviews = c.fetchall