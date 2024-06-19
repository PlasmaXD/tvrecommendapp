from database import get_all_reviews, get_program_details, add_program
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from scraper import get_program_details_from_scraper

def recommend_programs(user_id, n_recommendations=10):
    reviews = get_all_reviews()
    data = [(user, item, float(rating)) for user, item, rating in reviews]

    reader = Reader(rating_scale=(1, 5))
    dataset = Dataset.load_from_df(pd.DataFrame(data, columns=['user_id', 'program_id', 'rating']), reader)

    trainset, testset = train_test_split(dataset, test_size=0.25)

    algo = SVD()
    algo.fit(trainset)

    user_history = [item for (user, item, rating) in reviews if user == user_id]

    all_programs = list(set([item for (user, item, rating) in reviews]))

    unseen_programs = [item for item in all_programs if item not in user_history]

    predictions = [algo.predict(user_id, item) for item in unseen_programs]
    predictions.sort(key=lambda x: x.est, reverse=True)

    top_n_recommendations = predictions[:n_recommendations]
    recommended_programs_ids = [pred.iid for pred in top_n_recommendations]

    recommended_programs_details = get_program_details_by_ids(recommended_programs_ids)
    return recommended_programs_details

def get_program_details_by_ids(program_ids):
    details = []
    for program_id in program_ids:
        detail = get_program_details(program_id)
        if detail:
            details.append(detail)
        else:
            # デフォルト値を設定する場合はここでスクレイピング
            details.append({'url': '', 'title': f'Program {program_id}', 'supplement': f'Details of Program {program_id}'})
    return details

#スクレピングするから絶対大丈夫なパターン
# def get_program_details_by_ids(program_ids):
#     details = []
#     for program_id in program_ids:
#         detail = get_program_details(program_id)
#         if not detail:
#             # スクレイピングで詳細を取得し、データベースに保存
#             detail = get_program_details_from_scraper(program_id)
#             add_program(program_id, detail['url'], detail['title'], detail['supplement'])
#         details.append(detail)
#     return details