import streamlit as st
from scraper import get_program_details
from database import add_review, get_reviews, create_tables, add_user, get_user_favorites, add_favorite, add_program
from utils import extract_program_id
from recommendation import recommend_programs
import pandas as pd

# セッションステートを初期化
if 'search_word' not in st.session_state:
    st.session_state.search_word = ''
if 'program_data' not in st.session_state:
    st.session_state.program_data = []
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

def review_form(program_id, program_title, program_url, program_supplement, user_id):
    form_key = f"review_form_{program_id}"
    with st.form(key=form_key):
        rating = st.slider("評価", 1, 5, 3)
        review_text = st.text_area("レビューを入力してください")
        submit_button = st.form_submit_button("レビューを投稿")
        
        if submit_button:
            if user_id is not None:  # ユーザーIDがNoneでないことを確認
                add_review(program_id, program_title, user_id, rating, review_text)
                add_favorite(user_id, program_id)
                add_program(program_id, program_url, program_title, program_supplement)  # 番組詳細を保存
                st.success("レビューが投稿されました！")
                show_reviews(program_id)
            else:
                st.error("ユーザーIDが見つかりません。再度ログインしてください。")

def show_reviews(program_id):
    reviews = get_reviews(program_id)
    if reviews:
        st.subheader("レビュー")
        for review in reviews:
            st.write(f"ユーザーID: {review[0]}, 評価: {review[1]}星, レビュー: {review[2]}, 投稿日: {review[3]}")
    else:
        st.write("この番組にはまだレビューがありません。")

def main():
    create_tables()  # アプリケーション起動時にテーブルを作成
    st.title('番組情報と共演者検索')

    login_section = st.sidebar
    login_section.subheader("ログイン")
    if st.session_state.logged_in_user:
        login_section.write(f"ログイン中: {st.session_state.logged_in_user}")
    else:
        user_id = login_section.text_input("ユーザーID")
        user_name = login_section.text_input("ユーザー名")
        login_button = login_section.button("ログイン")

        if login_button:
            if user_id and user_name:
                add_user(user_id, user_name)
                st.session_state.logged_in_user = user_id
                st.sidebar.success(f"ようこそ、{user_name}さん！")
                print(f"User logged in: {user_id}")
            else:
                st.sidebar.error("ユーザーIDとユーザー名を入力してください。")

    if st.session_state.logged_in_user:
        st.sidebar.subheader("おすすめの番組")
        recommendations = recommend_programs(st.session_state.logged_in_user)
        print(f"Recommendations for user {st.session_state.logged_in_user}: {recommendations}")
        if recommendations:
            for rec in recommendations:
                st.sidebar.write(f"番組名: {rec['title']}")
                st.sidebar.write(f"情報: {rec['supplement']}")
        else:
            st.sidebar.write("おすすめ番組が見つかりませんでした。")

    search_word = st.text_input("検索ワードを入力してください", st.session_state.search_word)
    if st.button('検索'):
        st.session_state.search_word = search_word
        st.session_state.program_data = get_program_details(search_word)

    for program in st.session_state.program_data:
        program_id = extract_program_id(program['url'])  # URLから番組IDを抽出
        program_title = program['title']
        program_url = program['url']
        program_supplement = program['supplement']
        st.write(f"番組名: {program_title}")
        st.write(f"情報: {program_supplement}")
        st.write("共演者:")
        for name in program['cast_names']:
            st.write(f" - {name}")
        st.write("\n")

        # レビュー投稿フォームとレビュー表示
        review_form(program_id, program_title, program_url, program_supplement, st.session_state.logged_in_user)
        show_reviews(program_id)

if __name__ == "__main__":
    main()
